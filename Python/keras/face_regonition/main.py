from abc import ABCMeta, abstractmethod
from PIL import Image, ImageDraw
from llh.Python.keras.face_regonition.input.crop_image import crop
from llh.Python.keras.face_regonition.output.classifier import predict

class Function(metaclass = ABCMeta):
     def __init__(self,name):
          self.name = name

     @abstractmethod
     def execute(func):
          pass
     
class Input(Function):
     def __init__(self,name):
          super(Input,self).__init__(name)
     def execute(self,func):
          func.filename = input('Please Input the image name:(including file name)')
          try:
               func.image = Image.open(func.filename, 'r')
               print('Input Successful!')
          except FileNotFoundError:
               print('No file ',filenmae,'in this directory')

class Calculate(Function):
     def __init__(self,name):
          super(Calculate,self).__init__(name)
     def execute(self,func):
          draw = ImageDraw.Draw(func.image)
          output = []
          plist = []
          for scale in range (2,10):
               size = scale * 25
               crop_list = (crop(func.image, (int(size*0.7) , size), 4))
               output.extend(predict('12-net-calibration',crop_list,func.image))
                            
          for box in output:
               draw.rectangle(box, outline='red')
          func.image.show()

class Save(Function):
     def __init__(self,name):
          super(Save,self).__init__(name)
     def execute(self,func):
          savename = func.filename.split('.')
          try:
               func.image.save(savename[0]+'_result.'+savename[1])
          except:
               print('Saving Erorr !')
          
class Exit(Function):
     def __init__(self,name):
          super(Exit,self).__init__(name)
     def execute(self,func):
          exit()
     
class Program(Function):
     def __init__(self,name):
          self.name = name
          self.flist = [Exit('Exit.')]
          self.exit = False
          self.filename = None
          self.image = None

     def execute(self):
          while self.exit != True:
               print('\n Welcome to',self.name,'Program !')
               print('You can choose following function:')
               self.show()
               answer = input()
               self.flist[int(answer)-1].execute(self)
               try:
                    pass
               except:
                    print('Wrong number of Function!')
                    continue
               
     def add(self,function):
          self.flist.insert(len(self.flist)-1,function)

     def show(self):
          for index,func in enumerate(self.flist):
               print(index+1,'.',func.name)



if __name__ == "__main__":
     p = Program('Face Detection')
     p.add(Input('Input the image.'))
     p.add(Calculate('Calculate & Show the result.'))
     p.add(Save('Save the result.'))
     p.execute()

