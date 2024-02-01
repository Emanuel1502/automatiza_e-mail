import time
import datetime

# Bibliotecas selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Bibliotecas smtp para o Gmail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

print("Inicializando o programa...")
time.sleep(0.30)
print()
pesquisa = input("Pesquisar previsão do dia (D) ou da semana (S) ? ")

#verifica a escolha do usuário
if pesquisa == "D" or pesquisa == "d":
    #faz o procedimento para a previsão do tempo do dia específico
    print()
    print("NÃO É POSSÍVEL IDENTIFICAR PREVISÃO DO TEMPO DE DIAS PASSADOS!!!")
    previsao = input("Realizar a busca da previsão do tempo de qual data? (DD/MM/YYYY): ")
    cidade = input("Qual cidade desejada? ")
    print()
    print("iniciando a pesquisa...")
    time.sleep(0.30)

    #abre o chromedriver e abre o google
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.google.com")

    wait = WebDriverWait(driver, 20)

    #seleciona o campo de pesquisa e digita a data e a cidade na qual irá pesquisar a previsão do tempo
    campo_pesquisa = driver.find_element_by_xpath("//textarea[@name='q']") 
    campo_pesquisa.clear()
    campo_pesquisa.send_keys("previsão do tempo dia %s na cidade de %s" % (previsao, cidade))
    campo_pesquisa.send_keys(Keys.ENTER)
    time.sleep(1)

    try:

        #tenta achar os campos que contém os dados da previsão
        temperatura = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[id='wob_tm']"))).text
        clima = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[id='wob_dc']"))).text
        chuva = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[id='wob_pp']"))).text
        umidade = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[id='wob_hm']"))).text
        vento = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[id='wob_ws']"))).text
        data_envio = datetime.date.today() #identifica a data em que o programa esta rodando
        data_envio = data_envio.strftime('%d/%m/%Y')#faz o tratamento da data
        time.sleep(1)
        driver.quit()


    #caso não encontrtar os elementos no tempo limite, exibe uma mensagem de erro
    except TimeoutException:
        print("Erro: Tempo limite excedido ao aguardar elementos na página.")
        driver.quit()
        exit()
    #se acontecer um erro na pesquisa, exibirá uma mensagem de erro contendo o problema ocorrido
    except Exception as erro:
        print("Erro: Ocorreu uma exceção durante a obtenção da previsão do tempo.")
        print(str(erro))
        driver.quit()
        exit()

    #mostra oa dados da previsão do tempo do dia 
    print()
    print("Previsão do tempo para o dia: %s" % previsao)
    print()
    print("Cidade: %s" % cidade)
    print()
    print("Temperatura: %s°C" % temperatura)
    print()
    print("Clima: %s" % clima)
    print()
    print("Chuva: %s" % chuva)
    print()
    print("Umidade: %s" % umidade)
    print()
    print("Vento: %s" % vento)
    print()
    print("Data da pesquisa: %s" % data_envio)

    try:
        #tenta conectar os dados com o e-mail para enviar os dados
        email_send = "roboemail40@gmail.com"
        email_receive = input("Digite os e-mails para quem deseja enviar a previsão do tempo, separe-os com vírgula: ")
        email_receive = email_receive.split(",") #cria uma lista com os e-mails inseridos pelo usuário e os separa pela vírgula

        #configura os campos necessários para o envio dos e-mails
        msg = MIMEMultipart()
        msg['From'] = email_send
        msg['To'] = ", ".join(email_receive)
        msg['Subject'] = "Previsão do tempo para o dia %s na cidade de %s" % (previsao, cidade)
        body = """A previsão do tempo para o dia %s na cidade de %s será a seguinte:

        Temperatura: %s °C
        Clima: %s
        Possibilidade de chuva: %s
        Umidade: %s
        Velocidade do vento: %s

        Data da pesquisa: %s

        """ % (previsao, cidade, temperatura, clima, chuva, umidade, vento, data_envio)

        msg.attach(MIMEText(body, 'plain'))

        # Servidor SMTP
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # Segurança
        s.starttls()

        #verifica o login
        s.login(email_send, 'hmmb evsb vpns xapq')

        text = msg.as_string()

        for email in email_receive:
            #envia a mensagem para cada email adicionado na lista
            s.sendmail(email_send, email.strip(), text)

        s.quit()
    #se o ocorrer um erro ao enviar os e-mails, exibirá uma mensagem de erro relatando o problema
    except Exception as erro:
        print("Erro: Ocorreu uma exceção durante o envio dos e-mails.")
        print(str(erro))
        driver.quit()
        exit()

#==============================================================================================================
        
#faz o procedimento para a previsão do tempo da semana
else:
    
    print()    
    print("Iniciando pesquisa da previsão do tempo da semana...")

    cidade = input("Qual cidade desejada? ")
    print()
    print("Iniciando a pesquisa...")
    time.sleep(0.30)

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://www.google.com")

    wait = WebDriverWait(driver, 20)

    previsao_semana = set() #cria o grupo para armazenar os dados da previsão da semana

    #seleciona o campo de pesquisa e realiza a busca da previsão da semana em determinada cidade
    campo_pesquisa = driver.find_element_by_xpath("//textarea[@name='q']")
    campo_pesquisa.clear()
    campo_pesquisa.send_keys("previsão do tempo na cidade de %s" % (cidade))
    campo_pesquisa.send_keys(Keys.ENTER)
    time.sleep(1)

    try:

        #cria a lista de dia e clima
        dias = []
        climas = []
        data_envio = datetime.date.today() #pega a data em que o programa está em funcionamento
        data_envio = data_envio.strftime('%d/%m/%Y') #faz a tratativa da data
        print()
        print("Data da pesquisa: %s"%data_envio)
        print()
        print("Cidade: %s"%cidade)
        

        for i in range(8):

            #percorre todas as divs que contem a previsão do tempo dos dias da semana
            div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-wob-di='%s']" % i)))

            #obtém e armazena os dados nas variáveis
            dia_element = div.find_element(By.CSS_SELECTOR, "div[class='Z1VzSb']")
            clima_element =div.find_element(By.CSS_SELECTOR, "img[class='YQ4gaf zr758c']")

            #atribui o valor dos elementos do html às variáveis
            dia = dia_element.get_attribute("aria-label")
            clima = clima_element.get_attribute("alt")

            #adiciona os dados nas listas
            dias.append(dia)
            climas.append(clima)
        driver.quit()
        corpo = ""

        for i in range(8):
            #cria o corpo do e-mail concatenando os dados da previsão 
            corpo += "%s: %s\n" % (dias[i], climas[i])
            print()
            print("%s: %s" % (dias[i], climas[i]))

        try:

            #tenta conectar para mandar o email
            email_send = "roboemail40@gmail.com"
            print()
            email_receive = input("Digite os e-mails para quem deseja enviar a previsão do tempo, separe-os com vírgula: ")
            email_receive = email_receive.split(",")
            msg = MIMEMultipart()
            msg['From'] = email_send
            msg['To'] = ", ".join(email_receive)
            msg['Subject'] = "Previsão do tempo para a semana do dia %s na cidade de %s" % (data_envio, cidade)
            body = """Previsão do tempo para a semana do dia %s na cidade de %s:

%s


            """ %(data_envio,cidade,corpo)

            msg.attach(MIMEText(body, 'plain'))

            # Servidor SMTP
            s = smtplib.SMTP('smtp.gmail.com', 587)

            # Segurança
            s.starttls()

            s.login(email_send, 'hmmb evsb vpns xapq')

            text = msg.as_string()

            for email in email_receive:
                #envia a previsão do tempo da semana para os e-mails informados
                s.sendmail(email_send, email.strip(), text)

            print()
            print("E-mails enviados com sucesso.")

            s.quit()


        #se nao conseguir conectar, exibirá uma mensagem de erro contendo o problema ocorrido 
        except Exception as erro:
            print("Erro: Ocorreu uma exceção durante o envio dos e-mails.")
            print(str(erro))
            s.quit()
            exit()  

        
        
    #se não encontrar os elementos do html no tempo limite, exibirá uma mensagem de erro                
    except TimeoutException:
        print("Erro: Tempo limite excedido ao aguardar elementos na página.")
        driver.quit()
        exit()

    #se ocorrer algum problema ao obter os dados da previsão do tempo,  exibirá uma mensagem contendo o problema ocorrido
    except Exception as erro:
        print("Erro: Ocorreu uma exceção durante a obtenção da previsão do tempo.")
        print(str(erro))
        driver.quit()
        exit()

    

