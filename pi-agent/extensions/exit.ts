import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.on("input", async (event, ctx) => {
    if (event.text.trim() !== "exit") return { action: "continue" };

    if (ctx.hasUI) {
      ctx.ui.notify("Exiting pi...", "info");
    }
    ctx.shutdown();
    return { action: "handled" };
  });
}
