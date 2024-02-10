import wx
import logging
import os
import openai
import json
from ..nlpmodels import az_openailib

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(800, 700))
        panel = wx.Panel(self)

        # Create widgets
        label0 = wx.StaticText(panel, label="Bot role:")
        self.botrole = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size= wx.Size(700,100))
        label1 = wx.StaticText(panel, label="User prompt:")
        self.userprompt = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size= wx.Size(700,100))
        label2 = wx.StaticText(panel, label="Enter your text:")
        self.text2sum = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size= wx.Size(700,400))
        label3 = wx.StaticText(panel, label="Text summary:")
        self.textsummary = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size= wx.Size(700,200))
        btngensummary = wx.Button(panel, label="Generate summary")

         # Set up the layout using sizers
        windowSizer = wx.BoxSizer()
        windowSizer.Add(panel, 1, wx.ALL | wx.EXPAND)

        # Set up the layout using GridBagSizer
        sizer = wx.GridBagSizer(vgap=10, hgap=5)
        sizer.Add(label0, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.botrole, pos=(0, 1), span=(1, 2), flag=wx.EXPAND)
        sizer.Add(label1, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.userprompt, pos=(1, 1), span=(1, 2), flag=wx.EXPAND)
        sizer.Add(label2, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.text2sum, pos=(3, 0), span=(1, 2), flag=wx.EXPAND)
        sizer.Add(label3, pos=(4, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.textsummary, pos=(5, 0), span=(1, 2), flag=wx.EXPAND)
        sizer.Add(btngensummary, pos=(6, 0), span=(1, 2), flag=wx.EXPAND)

        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.ALL | wx.EXPAND, 6)

        panel.SetSizerAndFit(border)
        self.SetSizerAndFit(windowSizer)

        # Bind the button click event to a handler
        btngensummary.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, e):
        # Generate summary for the text entered in the text to summarize box
        response = az_openailib.OpenAiApiRequest(prompt=self.userprompt,
                                         bot_role=self.botrole,
                                         data=self.text2sum.GetValue())
        
        if response['error']:
           self.textsummary.SetValue(f"[ERROR]:{response['error']}") 
        else:
            self.textsummary.SetValue(f"{response['summary']}")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, title="Get text summary with Open AI")
    frame.Show()
    app.MainLoop()


