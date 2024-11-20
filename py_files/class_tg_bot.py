from bot_function import *

class tg_bot:
   def __init__(self):
      self.commands_switch = {'start_server' :["sh sh_scripts/start_server.sh", "time_out_on", "all_users_message_on"],
                   'stop_server'             :["sh sh_scripts/stop_server.sh",  "time_out_on", "all_users_message_on"],
                   'status_server'           :["sh sh_scripts/status_server.sh","time_out_off","all_users_message_off"]}

      self.rcon_commands_switch = {'send_message'  : ["", "send_answer_off"],
                                   'players'       : ["/players",   "send_answer_on"],
                                   'server_save'   : ["/server-save", "send_answer_on"]
                                  }

      parameters_filename = 'data/parameters.txt'
      file_param = open(parameters_filename, 'r')
      lines_param = file_param.readlines()
      file_param.close()

      self.parameters_switch = {}
      for line in lines_param:
         line = line.split()
         self.parameters_switch[line[0]] = line[1]

      self.bot = telebot.TeleBot(self.parameters_switch['tg_token']) #токен бота
      self.time_last_call = datetime.datetime(2011,11,11,11,11)

      log_filename = str(datetime.datetime.now().strftime("logs/%Y_%m_%d_time_%H_%M_%S_bot.log"))
      logging.basicConfig(filename = log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      self.logger = logging.getLogger(__name__)

   def run_bot(self):
   ########BOT HELP########
      @self.bot.message_handler(commands=['start'])
      def start_bot(message):
         try:
            print_help(message, self)
            self.logger.info("User %s print command %s ", message.from_user.username, message.text)
         except Exception as e:
            self.logger.error(f"Ошибка при отправке сообщения в канал: {e}")

      @self.bot.message_handler(commands=['help'])
      def help_bot(message):
         try:
            print_help(message, self)
            self.logger.info("User %s print command %s ", message.from_user.username, message.text)
         except Exception as e:
            self.logger.error(f"User %s print command %s: {e}", message.from_user.username, message.text)

      #####SERVER CONTROL#####
      @self.bot.message_handler(commands=list(self.commands_switch.keys()))
      def control_server(message):
         try:
            command_executer(message, self)
            self.logger.info("User %s print command %s ", message.from_user.username, message.text)
         except Exception as e:
            self.logger.error(f"User %s print command %s: {e}", message.from_user.username, message.text)

      #######RCON COMMAND#######
      @self.bot.message_handler(commands=list(self.rcon_commands_switch.keys()))
      def rcon_command(message):
         try:
            rcon_command_executer(message, self)
            self.logger.info("User %s print command %s ", message.from_user.username, message.text)
         except Exception as e:
            self.logger.error(f"User %s print command %s: {e}", message.from_user.username, message.text)

      #@self.bot.message_handler(content_types=["text"])

      while True:
         try: #добавляем try для бесперебойной работы
            self.bot.polling(none_stop=True) #запуск бота
         except:
            time.sleep(10) #в случае падения
