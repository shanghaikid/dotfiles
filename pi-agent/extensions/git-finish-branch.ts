import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

function shellQuote(value: string): string {
  return `'${value.replace(/'/g, `'\\''`)}'`;
}

async function git(
  pi: ExtensionAPI,
  args: string[],
  cwd: string,
): Promise<string> {
  const result = await pi.exec("git", args, { cwd });
  if (result.code !== 0) {
    const output = [result.stdout, result.stderr]
      .filter(Boolean)
      .join("\n")
      .trim();
    throw new Error(
      output || `git ${args.join(" ")} failed with exit code ${result.code}`,
    );
  }
  return result.stdout.trim();
}

async function gitOk(
  pi: ExtensionAPI,
  args: string[],
  cwd: string,
): Promise<boolean> {
  const result = await pi.exec("git", args, { cwd });
  return result.code === 0;
}

async function localBranchExists(
  pi: ExtensionAPI,
  branch: string,
  cwd: string,
): Promise<boolean> {
  return gitOk(
    pi,
    ["show-ref", "--verify", "--quiet", `refs/heads/${branch}`],
    cwd,
  );
}

async function remoteBranchExists(
  pi: ExtensionAPI,
  branch: string,
  cwd: string,
): Promise<boolean> {
  return gitOk(
    pi,
    ["show-ref", "--verify", "--quiet", `refs/remotes/origin/${branch}`],
    cwd,
  );
}

async function defaultBranch(pi: ExtensionAPI, cwd: string): Promise<string> {
  const originHead = await pi.exec(
    "git",
    ["symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"],
    { cwd },
  );
  if (originHead.code === 0) {
    const branch = originHead.stdout.trim().replace(/^origin\//, "");
    if (branch === "main" || branch === "master") return branch;
  }

  for (const branch of ["main", "master"]) {
    if (
      (await localBranchExists(pi, branch, cwd)) ||
      (await remoteBranchExists(pi, branch, cwd))
    ) {
      return branch;
    }
  }

  throw new Error(
    "Could not find a main or master branch locally or on origin.",
  );
}

export default function (pi: ExtensionAPI) {
  pi.registerCommand("finish-branch", {
    description:
      "Switch to main/master, pull the latest changes, then delete the previous current branch. If the branch is not fully merged, ask before force-deleting. Use --force to skip that extra prompt.",
    handler: async (args, ctx) => {
      await ctx.waitForIdle();

      const cwd = ctx.cwd;
      const force = args.split(/\s+/).includes("--force");

      if (!(await gitOk(pi, ["rev-parse", "--is-inside-work-tree"], cwd))) {
        ctx.ui.notify("Not inside a Git repository.", "error");
        return;
      }

      const currentBranch = await git(pi, ["branch", "--show-current"], cwd);
      if (!currentBranch) {
        ctx.ui.notify(
          "You are in detached HEAD state; no current branch to delete.",
          "error",
        );
        return;
      }

      const targetBranch = await defaultBranch(pi, cwd);
      if (currentBranch === targetBranch) {
        ctx.ui.notify(
          `Already on ${targetBranch}; refusing to delete it.`,
          "error",
        );
        return;
      }

      const status = await git(pi, ["status", "--porcelain"], cwd);
      if (status) {
        ctx.ui.notify(
          "Working tree is not clean. Commit, stash, or discard changes before running /finish-branch.",
          "error",
        );
        return;
      }

      const confirmed = await ctx.ui.confirm(
        "Finish branch?",
        `Switch to ${targetBranch}, pull latest changes, then delete ${currentBranch}${force ? " with force if needed" : ""}?`,
      );
      if (!confirmed) return;

      ctx.ui.notify("Fetching origin...", "info");
      await git(pi, ["fetch", "--prune", "origin"], cwd);

      if (await localBranchExists(pi, targetBranch, cwd)) {
        await git(pi, ["switch", targetBranch], cwd);
      } else if (await remoteBranchExists(pi, targetBranch, cwd)) {
        await git(
          pi,
          [
            "switch",
            "--create",
            targetBranch,
            "--track",
            `origin/${targetBranch}`,
          ],
          cwd,
        );
      } else {
        throw new Error(
          `Could not find ${targetBranch} locally or on origin after fetch.`,
        );
      }

      ctx.ui.notify(`Pulling latest ${targetBranch}...`, "info");
      if (
        await gitOk(
          pi,
          ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
          cwd,
        )
      ) {
        await git(pi, ["pull", "--ff-only"], cwd);
      } else {
        await git(pi, ["pull", "--ff-only", "origin", targetBranch], cwd);
      }

      const isMerged = await gitOk(
        pi,
        ["merge-base", "--is-ancestor", currentBranch, targetBranch],
        cwd,
      );

      let deleteFlag = "-d";
      if (!isMerged) {
        if (!force) {
          const uniqueCommits = await git(
            pi,
            ["log", "--oneline", `${targetBranch}..${currentBranch}`],
            cwd,
          );
          const commitLines = uniqueCommits
            .split("\n")
            .filter(Boolean)
            .slice(0, 10)
            .join("\n");
          const forceConfirmed = await ctx.ui.confirm(
            "Branch is not fully merged",
            `${currentBranch} has commits that are not in ${targetBranch}.\n\n${commitLines || "(no commit details available)"}\n\nForce-delete this local branch?`,
          );
          if (!forceConfirmed) {
            ctx.ui.notify(
              `Kept ${shellQuote(currentBranch)} because it is not fully merged.`,
              "info",
            );
            return;
          }
        }
        deleteFlag = "-D";
      }

      await git(pi, ["branch", deleteFlag, currentBranch], cwd);

      ctx.ui.notify(
        `Done: switched to ${targetBranch}, pulled latest changes, and ${deleteFlag === "-D" ? "force-deleted" : "deleted"} ${shellQuote(currentBranch)}.`,
        "success",
      );
    },
  });
}
