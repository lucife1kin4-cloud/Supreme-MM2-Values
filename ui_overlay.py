local Players = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")
local LocalPlayer = Players.LocalPlayer

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "MM2ValueCheckerUI"
ScreenGui.ResetOnSpawn = false

if syn and syn.protect_gui then
syn.protect_gui(ScreenGui)
ScreenGui.Parent = CoreGui
elseif gethui then
ScreenGui.Parent = gethui()
else
ScreenGui.Parent = CoreGui
end

local MainFrame = Instance.new("Frame")
MainFrame.Size = UDim2.new(0, 240, 0, 130)
MainFrame.Position = UDim2.new(0.05, 0, 0.35, 0)
MainFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
MainFrame.BorderSizePixel = 0
MainFrame.Active = true
MainFrame.Draggable = true
MainFrame.Parent = ScreenGui

local UICorner = Instance.new("UICorner")
UICorner.CornerRadius = UDim.new(0, 8)
UICorner.Parent = MainFrame

local Title = Instance.new("TextLabel")
Title.Size = UDim2.new(1, 0, 0, 30)
Title.BackgroundTransparency = 1
Title.Text = "MM2 Trade Checker"
Title.TextColor3 = Color3.fromRGB(255, 255, 255)
Title.TextSize = 15
Title.Font = Enum.Font.SourceSansBold
Title.Parent = MainFrame

local MyValueLabel = Instance.new("TextLabel")
MyValueLabel.Size = UDim2.new(1, -20, 0, 22)
MyValueLabel.Position = UDim2.new(0, 10, 0, 35)
MyValueLabel.BackgroundTransparency = 1
MyValueLabel.Text = "ВАШИ ПРЕДМЕТЫ: 0"
MyValueLabel.TextColor3 = Color3.fromRGB(85, 255, 127)
MyValueLabel.TextSize = 13
MyValueLabel.Font = Enum.Font.SourceSans
MyValueLabel.TextXAlignment = Enum.TextXAlignment.Left
MyValueLabel.Parent = MainFrame

local TheirValueLabel = Instance.new("TextLabel")
TheirValueLabel.Size = UDim2.new(1, -20, 0, 22)
TheirValueLabel.Position = UDim2.new(0, 10, 0, 60)
TheirValueLabel.BackgroundTransparency = 1
TheirValueLabel.Text = "ИХ ПРЕДМЕТЫ: 0"
TheirValueLabel.TextColor3 = Color3.fromRGB(255, 85, 85)
TheirValueLabel.TextSize = 13
TheirValueLabel.Font = Enum.Font.SourceSans
TheirValueLabel.TextXAlignment = Enum.TextXAlignment.Left
TheirValueLabel.Parent = MainFrame

local StatusLabel = Instance.new("TextLabel")
StatusLabel.Size = UDim2.new(1, -20, 0, 22)
StatusLabel.Position = UDim2.new(0, 10, 0, 90)
StatusLabel.BackgroundTransparency = 1
StatusLabel.Text = "Статус: Ожидание трейда..."
StatusLabel.TextColor3 = Color3.fromRGB(180, 180, 180)
StatusLabel.TextSize = 12
StatusLabel.Font = Enum.Font.SourceSansItalic
StatusLabel.TextXAlignment = Enum.TextXAlignment.Left
StatusLabel.Parent = MainFrame
