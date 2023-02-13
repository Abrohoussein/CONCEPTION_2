
import datetime
import time
import threading
import random
import functools

cpt = 0
lock = threading.Lock()
my_threads = []
global preempted
preempted = False
################################################################################
#   Watchdog to stop tasks
################################################################################
class EDF(threading.Thread):

        def __init__(self):
            # Initialisation du scheduler
            print("\nScheduler Initialisation : " + datetime.datetime.now().strftime("%H:%M:%S"))
            self.task_list = []
            self.cpt_T3 = 0
            self.cpt_T4 = 0
            self.current_task = None
            self.current_task_state = None # R pour Running, F pour finished
            self.preempt = 0
            threading.Thread.__init__(self)
            
        # La fonction est applé add périodiquement
        # ajoute les tâches à éxécuté dans la liste des tâches
        # utilisée par le scheduler
        def add_tasks(self):
            
           
            
            # Toute les 10 secondes nous ajoutons les taches T1 et T2 en début de liste en raison de leur priorité
            self.task_list.insert(0,my_task(name="Motors Control", period=10, execution_time=1, last_execution=last_execution, preemptable=False))
            print(datetime.datetime.now().strftime("%H:%M:%S"),"  Task - Motors Control added to tasks list")
            
            self.task_list.insert(0,my_task(name="Sensor Acquisition", period=10, execution_time=1, last_execution=last_execution,preemptable=False))
            print(datetime.datetime.now().strftime("%H:%M:%S"),"  Task - Sensor Acquisition added to tasks list")

            # A l'aide d'un compteur la tâche T3 est ajouté
            # toute les 30s à la liste des tâches
            if self.cpt_T3 == 3 or self.cpt_T3 == 0 :
                self.cpt_T3 = 0
                self.task_list.append(my_task(name="Camera Analysis", period=30, execution_time=20, last_execution=last_execution,preemptable=True))
                print(datetime.datetime.now().strftime("%H:%M:%S"),"  Task - Camera Analysis added to tasks list")
                
            # La tâche T4 toute les 60s
            if self.cpt_T4 == 6 or self.cpt_T4 == 0 :
                self.cpt_T4 = 0
                self.task_list.append(my_task(name="Transmission system", period=60, execution_time=20, last_execution=last_execution,preemptable=True))
                print(datetime.datetime.now().strftime("%H:%M:%S"),"  Task - Transmission system added to tasks list")
            
            self.cpt_T3 +=1
            self.cpt_T4 +=1
           

        
            
        def run(self):
                
                with lock:
            
                    while (len(self.task_list)<4):
                            1+1
                    if self.current_task_state == None and self.current_task == None :
                        self.current_task_state = 'R'
                        self.current_task = self.task_list[0].name
                        self.task_list[0].run(self)
                    while True:
                            if self.current_task_state == 'R' and self.current_task != self.task_list[0].name:

                                
                                self.current_task = self.task_list[0].name
                                self.task_list[0].run(self)
                            if self.current_task_state == 'R' and self.current_task == self.task_list[0].name and self.task_list[0].preempted == True:

                                
                                self.current_task = self.task_list[0].name
                                self.task_list[0].run(self)
                                
                            if self.current_task_state == 'F' and self.current_task == self.task_list[0].name:
                                
                                print(datetime.datetime.now().strftime("%H:%M:%S")," -------- Task ",self.task_list[0].name," Finished")
                                if ( self.current_task == "Transmission system" ):
                                    exit
                                self.task_list.pop(0)
                                self.current_task = self.task_list[0].name
                                self.current_task_state == 'R'
                                self.task_list[0].run(self)

                            


                    
# Cette fonction auxilliaire lance un premier thread pour éxécuté la fonction add_tasks
# puis se reéxécute de manière récurcive après un temps d'arret de 10s 
def add_periodically(EDF):
                
    thread = threading.Thread(target = EDF.add_tasks)
            
    thread.start()
    add_thread = threading.Timer(10, functools.partial(add_periodically,EDF))
            
    add_thread.start()
    my_threads.append(thread)
    my_threads.append(add_thread)
    
################################################################################
#   Class simulant l'éxécution des tâches
################################################################################

class my_task():
    name = None
    period = -1
    execution_time = -1
    last_deadline = -1
    last_execution_time = None
    preemptable_count = 0

    def __init__(self, name, period, execution_time, last_execution, preemptable):
            
        self.name = name
        self.period = period
        self.execution_time = execution_time
        self.last_execution_time = last_execution
        self.enddate = datetime.datetime.now()+datetime.timedelta(seconds=period)
        self.preempted = False
        self.remainging_exec_time = -1
        self.preemptable = preemptable
            
    def run(self,scheduler):
        # Têche non premptive
        if ( self.name == "Sensor Acquisition" ):
                
            print(datetime.datetime.now().strftime("%H:%M:%S"),"  T1 - Sensor Acquisition starting ....")
            time.sleep(self.execution_time)
            scheduler.current_task_state = "F"
            
        # Têche non premptive    
        if ( self.name == "Motors Control" ):
                
            print(datetime.datetime.now().strftime("%H:%M:%S"),"  T2 - Motors Control starting ....")
            time.sleep(self.execution_time)
            scheduler.current_task_state = "F"
            
        # Têche premptive   
        if ( self.name == "Camera Analysis" ):

            print(datetime.datetime.now().strftime("%H:%M:%S"),"  T3 - Camera Analysis starting ....")
            if ( self.preemptable_count < 3):
                    time.sleep(8)
                    scheduler.current_task_state = "R"
                    self.preemptable_count +=2
                    self.preempted = True
            else:
                    time.sleep(4)
                    scheduler.current_task_state = "F"
                    self.preemptable_count +=0
                    
        # Têche premptive
        if ( self.name == "Transmission system" ):
                
            print(datetime.datetime.now().strftime("%H:%M:%S"),"  T3 - Transmission system starting ....")
            if ( self.preemptable_count < 19):
                    time.sleep(4)
                    scheduler.current_task_state = "R"
                    self.preemptable_count +=4
                    self.preempted = True
            else:
                    time.sleep(4)
                    scheduler.current_task_state = "F"
                    self.preemptable_count +=0


####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':
    
    last_execution = datetime.datetime.now()
    
    scheduler = EDF()
    scheduler.start()
    add_periodically(scheduler)
    
    
    scheduler.run()
    
    my_threads.append(scheduler)
    
    
        


