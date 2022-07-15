import win32com.client
import random
import sys
import time

def main():

    cf_path = r'C:\Users\josep\anaconda3\envs\ZF_attention_project\ppt_method\cf_presentation.pptx'
    dfm_path = r'C:\Users\josep\anaconda3\envs\ZF_attention_project\ppt_method\dfm_presentation.pptx'
    ufm_path = r'C:\Users\josep\anaconda3\envs\ZF_attention_project\ppt_method\ufm_presentation.pptx'

    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = 1

    class PptPres():
        def __init__(self, file_path):
            self.prs = app.Presentations.Open(FileName=file_path)
            self.path = file_path
        def runPPT(self):
            self.run = app.ActivePresentation.SlideShowSettings.Run()
            self.count = app.ActivePresentation.Slides.Count
            self.slides = app.ActivePresentation.Slides.Range(range(1,self.count+1))
            #self.slide = app.ActivePresentation.SlideShowWindow.View.Slide.SlideNumber
            for slide in self.slides:
                print(slide.SlideNumber)

        def closePPT(self):
            self.close = app.Presentations.Close(FileName=self.path)


        '''
        #trying to stop at last slide to end show, randomize ITI and then start next random show
        if p.slide == p.count:
            app.Quit()'''

    cf_prs = PptPres(cf_path)
    cf_prs.runPPT()

    time.sleep(20)

    app.SlideShowWindows(1).View.Exit()
    dfm_prs = PptPres(dfm_path)
    dfm_prs.runPPT()

    time.sleep(20)

    app.SlideShowWindows(1).View.Exit()
    ufm_prs = PptPres(ufm_path)
    ufm_prs.runPPT()


if __name__ == '__main__':
    main()