import System.Exit
import XMonad
import XMonad.Config.Desktop
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.EZConfig (additionalKeys) 

main = xmonad $ desktopConfig 
	{
		terminal	 = myTerminal,
		modMask		 = mod4Mask,
		normalBorderColor = myNormalBorderColor,
		focusedBorderColor = myFocusedBorderColor
	}
	`additionalKeys` [((mod4Mask, xK_p), spawn "rofi -show run")]

myTerminal = "urxvt"
myNormalBorderColor = "#090300"
myFocusedBorderColor = "#01a252"


