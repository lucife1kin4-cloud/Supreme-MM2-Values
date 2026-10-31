print("load starting")

local success, result = pcall(function()
return game:HttpGet("https://raw.githubusercontent.com/YourUsername/YourRepo/main/ui_overlay.lua")
end)

if success and result then
local loadedFunc, err = loadstring(result)
if loadedFunc then
loadedFunc()
print("MM2 Value Overlay loaded successfully.")
else
warn("Failed to compile UI script: " .. tostring(err))
end
else
warn("Failed to fetch UI script from remote source.")
end
