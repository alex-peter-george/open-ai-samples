import wx
import logging
import os
import openai
import json
from embeddings import correlate_docs

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
        label0 = wx.StaticText(panelA, label="Web Scrape URL:")
        self.siteurl = wx.TextCtrl(panelA, style=wx.TE_MULTILINE, size= wx.Size(700,50))
        self.siteurl.SetValue("https://www.indeed.com/jobs?q=python&l=New+York%2C+NY&vjk=8bf2e735050604df")
        label1 = wx.StaticText(panelA, label="Source document file:")
        sampleList = ['zero', 'one', 'two', 'three', 'four', 'five']
        cbfiles = wx.ComboBox(panelA, -1, "default value", (90, 50), (160, -1), sampleList, wx.CB_DROPDOWN)
        
        
        label2 = wx.StaticText(panelB, label="Source document content:")
        self.sourcedoc = wx.TextCtrl(panelB, style=wx.TE_MULTILINE, size= wx.Size(700,400))
        label3 = wx.StaticText(panelB, label="Bot response:")
        self.botresponse = wx.TextCtrl(panelB, style=wx.TE_MULTILINE, size= wx.Size(700,200))
        
        # Customize the appearance of "ask the bot" button to stand out
        btnaskbot = wx.Button(panelA, label="Ask the Bot")
        btnaskbot.SetBackgroundColour(wx.Colour(255, 230, 200))  # Set the background color
        # Create a bold font
        font = wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        btnaskbot.SetFont(font)

        sizerA.Add(label0, flag=wx.ALL, border=5)
        sizerA.Add(self.siteurl, flag=wx.ALL, border=5)
        sizerA.Add(label1, flag=wx.ALL, border=5)
        sizerA.Add(cbfiles, flag=wx.ALL, border=5)
      
        sizerA.Add(btnaskbot, flag=wx.ALL, border=5)

        sizerB.Add(label2, flag=wx.ALL, border=5)
        sizerB.Add(self.sourcedoc, flag=wx.ALL, border=5)
        sizerB.Add(label3, flag=wx.ALL, border=5)
        sizerB.Add(self.botresponse, flag=wx.ALL, border=5)

        # Arrange the panels side by side using a horizontal sizer
        winsizer = wx.BoxSizer(wx.HORIZONTAL)
       
        winsizer.Add(panelA, 1, wx.EXPAND)
        winsizer.Add(panelB, 2, wx.EXPAND)
        self.SetSizer(winsizer)

        # Bind the buttons click event to handlers
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
        # Generate scraped web document

        response = correlate_docs.RunWebScrape(self.siteurl.GetValue())
        if response['error']:
           self.botresponse.SetValue(f"[ERROR]:{response['error']}") 
        else:
            self.botresponse.SetValue(f"{response['response']}")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, title="Engage Bot with Open AI")
    frame.Show()
    app.MainLoop()


