import wx
import logging
import os
import openai
import json
from nlpmodels import az_openailib

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(1400, 700))

        # Create two panels
        panelA = wx.Panel(self)
        sizerA = wx.BoxSizer(wx.VERTICAL)
        panelA.SetSizer(sizerA)

        panelB = wx.Panel(self)
        sizerB = wx.BoxSizer(wx.VERTICAL)
        panelB.SetSizer(sizerB)
        
        # Create full set of controls to populate the main form
        label0 = wx.StaticText(panelA, label="Bot role:")
        self.botrole = wx.TextCtrl(panelA, style=wx.TE_MULTILINE, size= wx.Size(700,50))
        label1 = wx.StaticText(panelA, label="User prompt:")
        self.userprompt = wx.TextCtrl(panelA, style=wx.TE_MULTILINE, size= wx.Size(700,50))
        label2 = wx.StaticText(panelB, label="Enter your text:")
        self.usertext = wx.TextCtrl(panelB, style=wx.TE_MULTILINE, size= wx.Size(700,400))
        label3 = wx.StaticText(panelB, label="Bot response:")
        self.botresponse = wx.TextCtrl(panelB, style=wx.TE_MULTILINE, size= wx.Size(700,200))
        
        # Customize the appearance of "ask the bot" button to stand out
        btnaskbot = wx.Button(panelA, label="Ask the Bot")
        btnaskbot.SetBackgroundColour(wx.Colour(255, 230, 200))  # Set the background color
        # Create a bold font
        font = wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        btnaskbot.SetFont(font)

        self.defaultbotrole = wx.Button(panelA, label="Default bot role")
        self.userprompt_summary = wx.Button(panelA, label="Default user prompt: text summary")
        self.userprompt_sentiment = wx.Button(panelA, label="Default user prompt: text sentiment analysis")

        sizerA.Add(label0, flag=wx.ALL, border=5)
        sizerA.Add(self.botrole, flag=wx.ALL, border=5)
        sizerA.Add(self.defaultbotrole, flag=wx.ALL, border=5)

        sizerA.Add(label1, flag=wx.ALL, border=5)
        sizerA.Add(self.userprompt, flag=wx.ALL, border=5)

        # Create a grid sizer
        btnsizer = wx.GridSizer(cols=2)
        btnsizer.Add(self.userprompt_summary, flag=wx.EXPAND | wx.ALL, border=5)
        btnsizer.Add(self.userprompt_sentiment, flag=wx.EXPAND | wx.ALL, border=5)

        sizerA.Add(btnsizer)

        sizerA.Add(btnaskbot, flag=wx.ALL, border=5)

        sizerB.Add(label2, flag=wx.ALL, border=5)
        sizerB.Add(self.usertext, flag=wx.ALL, border=5)
        sizerB.Add(label3, flag=wx.ALL, border=5)
        sizerB.Add(self.botresponse, flag=wx.ALL, border=5)

        # Arrange the panels side by side using a horizontal sizer
        winsizer = wx.BoxSizer(wx.HORIZONTAL)
       
        winsizer.Add(panelA, 1, wx.EXPAND)
        winsizer.Add(panelB, 2, wx.EXPAND)
        self.SetSizer(winsizer)

        # Bind the buttons click event to handlers
        self.defaultbotrole.Bind(wx.EVT_BUTTON, self.OnDefaultBotroleButton)
        self.userprompt_summary.Bind(wx.EVT_BUTTON, self.OnUserePromptSummaryButton)
        self.userprompt_sentiment.Bind(wx.EVT_BUTTON, self.OnUserePromptSentimentButton)
        btnaskbot.Bind(wx.EVT_BUTTON, self.OnAskBotButton)

    def OnDefaultBotroleButton(self, e):
        # Populate the bot role to generate summary
        self.botrole.SetValue("You are a system chatbot that responds to a prompt entered by the user in a precise, concise manner, that assumes the user is an educatyed, mature person.")
    
    def OnUserePromptSummaryButton(self, e):
        # Populate the bot role to generate summary
        self.userprompt.SetValue("Extract the summary from the text that I entered.")

    def OnUserePromptSentimentButton(self, e):
        # Populate the bot role to generate summary
        self.userprompt.SetValue("Run a sentiment analysis against the text that I entered.")
    
    def OnAskBotButton(self, e):
        # Generate summary for the text entered in the text to summarize box
        response = az_openailib.OpenAiApiRequest(prompt=self.userprompt,
                                         bot_role=self.botrole,
                                         data=self.botresponse.GetValue())
        if response['error']:
           self.botresponse.SetValue(f"[ERROR]:{response['error']}") 
        else:
            self.botresponse.SetValue(f"{response['response']}")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, title="Engage Bot with Open AI")
    frame.Show()
    app.MainLoop()


