from subprocess import check_output
from rcon.source import Client
import telebot
import time
import datetime
import math
import os
import logging

def print_help(message, tg_bot_self):
   text_str = "SERVER CONTROL\n"
   mass = list(tg_bot_self.commands_switch.keys())
   for i in mass:
      text_str = text_str + '/' + i + '\n'

   text_str = text_str + "\nRCON COMMAND\n"
   mass = list(tg_bot_self.rcon_commands_switch.keys())
   for i in mass:
      text_str = text_str + '/' + i + '\n'

   tg_bot_self.bot.send_message(message.chat.id, text_str)

def collect_data_user(message, tg_bot_self):
   users_filename = tg_bot_self.parameters_switch['users_filename']
   if(os.path.isfile(users_filename) == False):
      with open(users_filename, 'w') as fp:
         pass

   file_str = open(users_filename, 'r')
   lines = file_str.readlines()
   #tg_bot_self.bot.send_message(message.chat.id, str(lines))
   file_str.close()

   str_user = str(message.chat.id) + ' ' + message.from_user.first_name \
              + ' ' + message.from_user.last_name + ' ' +message.from_user.username + '\n'

   #tg_bot_self.bot.send_message(message.chat.id, str_user)
   if((str_user in lines) == False):
      file_str = open(users_filename, 'a')
      file_str.write(str_user)
      file_str.close()

def all_user_message(message, tg_bot_self, command, time_diff, time_out):
   users_filename = tg_bot_self.parameters_switch['users_filename']
   if(tg_bot_self.commands_switch[command[0]][2] == "all_users_message_on" and \
      not (tg_bot_self.commands_switch[command[0]][1] == "time_out_on" and time_diff < time_out)):
      file_str = open(users_filename, 'r')
      lines = file_str.readlines()
      #tg_bot_self.bot.send_message(message.chat.id, str(lines))
      file_str.close()

      for line in lines:
         id = int(line.split()[0])
         if(id == id): #!= message.chat.id):
            str_text = message.from_user.username + ": " + command[0]
            tg_bot_self.bot.send_message(id, str_text)

def rcon_command_executer(message, tg_bot_self):
   collect_data_user(message, tg_bot_self)

   command = message.text[1::].split()

   text = ''
   if(command[0] == 'send_message'):
      text = text + message.from_user.username + ':'
   text = text + " " + ' '.join(command[1::])

   rcon_ip = '127.0.0.1'
   with Client(rcon_ip, int(tg_bot_self.parameters_switch['rcon_port']), passwd = tg_bot_self.parameters_switch['rcon_password']) as client:
      response = client.run(tg_bot_self.rcon_commands_switch[command[0]][0] + text)

      if(tg_bot_self.rcon_commands_switch[command[0]][1] == "send_answer_on"):
         tg_bot_self.bot.send_message(message.chat.id, response)

def command_executer(message,  tg_bot_self):
   collect_data_user(message, tg_bot_self)

   command = message.text[1::].split()
   time_out = int(tg_bot_self.parameters_switch['time_out'])
   time_diff = (datetime.datetime.now() - tg_bot_self.time_last_call).total_seconds()
   text = tg_bot_self.commands_switch[command[0]][0] + " " + ' '.join(command[1::])
   #print(text)

   if(tg_bot_self.commands_switch[command[0]][1] == "time_out_off"):
      tg_bot_self.bot.send_message(message.chat.id, check_output(text, shell = True))
   else:
      if(time_diff >= time_out):
         tg_bot_self.bot.send_message(message.chat.id, check_output(text, shell = True))
         tg_bot_self.time_last_call = datetime.datetime.now()
      else:
         tg_bot_self.bot.send_message(message.chat.id, "Timeout: " + str(round(time_diff, 1)) + "/" + str(time_out))


   all_user_message(message, tg_bot_self, command, time_diff, time_out)
