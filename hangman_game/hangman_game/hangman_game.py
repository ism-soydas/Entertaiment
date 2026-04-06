#Adam Asmaca oyunu son hal 
#Bu oyun da amac rastgele kelimeleri asilan adam tam cizilmeden harfler veya direk tahmin ile dogru cevabi bulmaktir
#Gelistirilme asamasindadir
 
#Kutuphaneler
import random as rd
import time as t
import pandas as pd
import sys

#Sinif Mimarisi
class Hang_Man(object):
    def __init__(self):
        """   
              Bu alanda kullanıcıya uygun veri tablosunun degiskeni 
              Kullanıcının üzerinde tahminler bulunması için orijinal kelime ve
              Kullanıcının yaptığı işlemlerin harf mi değil mi diye test etmesi için bir 
              Dictionary yapısında harfler olacaktır
                                                                                  """
        self.df = None
        #Burada kullanicinin uzerinde kelime tahmin edecegi farklı konulara bagli veri tablosu gelecektir 
        self.orj_word = None
        #Burada kullanicinin istedigi kategoriye gore ileriki asamalarda rastgele kelime uretilecektir 
        self.miss_word = None
        #Burasi kullanicinin oynayacagi oyun alani olacaktir
        self.letters = {'A','B','C','Ç','D','E','F','G','Ğ','H','I','İ','J','K',
                        'L','M','N','O','Ö','P','R','S','Ş','T','U','Ü','V','Y','Z'}
        #self.letters self.words'da da bahsettigimiz gibi harf teyit isleminde kullanilacaktir
        self.deletiDictC = set()
        #self.deletiDict kismi kullanicinin kullandigi dogru harflerin gecici olarak tutuldugu bir kisimdir
        #PrbingLet ve CreateRandSent Fonksiyonunda ileride kullanılacaktır
        self.all_deli_Dict = set()
        #kullanicin oyun da kullandigi tum harfleri gosterir
        #PrbingLet Fonksiyonunda ileride kullanılacaktır
        
    def drawing_man(self,hak):
        """   Burada kullanıcının hata yapmasına bağlı olarak adam çizilme işlemi yapılacaktır   """

        if hak == 1:
            return """
                  |
                  |
                  |
                  |"""
        elif hak == 2:
            return """
                   ___
                  |
                  |
                  |
                  |"""
        elif hak == 3:
            return """
                   ___
                  |  o
                  |
                  |
                  |"""
        elif hak == 4:
            return """
                   ___
                  |  o
                  | /\
                  |
                  |"""
        elif hak == 5:
            return """
                   ___
                  |  o
                  | /\
                  | /\ 
                  |"""
    def copy_of_letters_table(self):
        """
              Alternatif harf tablosu olusturma 
                                               """
        return self.letters.copy()
        #Burada kullanicin kullanmasi icin bir harf tablosu olusturuyoruz
        #Asil hedef referans degerimiz olan self.letters dictionary yapisini kaybetmeyerek islem yapmaktir
        
    def begin_of_game(self):
        
        """      
               Burada oyun tekrarı için eski alanı sıfırlama işlemi 
               veya kullanıcı oyuna daha yeni başlayacak ise başlangıç
               oluşturma işlemi yapılacaktır self.miss_word bu işlevi görecektir
                                                                       """
        self.miss_word = ""
        #Gecici tablomuzu olusturacaktir
        
    def message_end_of_game(self,_mess):
        return "Tebrikler Oyunu kazandınız :)" if _mess < 5 else "Oyunu kaybettiniz :("
        #Burada kullaniciya kalan haklarina gore oyun sonu mesaji verilecektir
        
    def create_space_of_game_for_random_word(self,l,ct):
        
        """   
              Burada kullanıcının her bir harf veya kelime tahminine göre kullanıcının
              ilerlemesini anlaması için belirli bir kelime alanı olacaktır
              ve ilerlemeye bağlı olarakta seçilen harfler bir bölmede çıkartılıp 
              (Farklı bir fonksiyonda kısaca) kullanıcıya hangi harflerin kullanılıp 
              kullanılmadığı gösterilecektir                               """
        result_mes,cont = None,None
        #result_mes oyundaki hamleye bagli olarak cikan sonucu gosterir
        #cont ise user_space olan main fonksiyonunu icin hatalı mesajini verir 
        #Bunun sonucunda da eger kelime de bu harf varsa veya onceden kullanildiysa hak degiskeninin degeri artar
        #Eger kullanicinin girdigi yeni kelime ilk defa kullanildiysa ve kelime de geciyorsa sonuc True donecektir
        
        prev_size_dDC= len(list(self.deletiDictC))
        #Ileride yeni dictionary yapisi ile eski yapiyi boyutsal olarak karsilastirmak için kullanilacaktir    
        for lets in self.orj_word:
            cont_spc = True
            #cont_spc Burada kelime arasinda bosluk var mi yok mu kontrol edecektir
            
            if lets == " ":
                self.miss_word += '|'
                cont_spc = False
            #lets == " " ile kelime de ki boslugu tespit ederek kosul icine atiyoruz
            #ve o boslugu ifade etmek icin self.miss_word'a | isaretini ekliyoruz
            #cont_spc ise burada bosluk bulundugundan dolayi _ isaretini koymayi engelleyen kosul olacaktir
            
            if lets in self.deletiDictC:
                self.miss_word += lets
            #Burada eger harf onceden kullanildiysa bu harfin kelime de var olup olmadigi kontrol edilir
            #Kontrol asamasindan sonra onceden varsa yazdirilir
            
            elif l == lets and l not in self.deletiDictC:
                self.miss_word += self.is_new_correct_letter(lets)
                result_mes,cont = self.messages_which_is_per_step_of_game('Correct') , True
            #Burada ise ilk olarak kelimedeki harf ile kullanicinin girdigi harf aynilar mı kontrol edilir
            #Eger harfler ayni ise ve bu harf daha onceden kullanilmadiysa self.is_new_correct_letter() fonksiyonuna yonlendilirilir
            #Bu fonksiyonu kisaca ozetlersek kullanilan harfi artik kullanildi diye isaretler ve o harfi oyun ekranina yazdirir
            #self.Message_Ins_o_Gm() fonskiyonu ise oyun ici gelismelere gore mesaj gonderir ve dogru kelime oldugu icin cont = True olur            
            
            elif l != lets and cont_spc:
                self.miss_word += '_'
            #Eger harf onceden kullanilmadiysa ve kelime ile de uyusmuyorsa _ yazdiracaktir
            #cont_spc ise burada eger rastgele kelimede bosluk varsa bunu belirtmek icin | bu isareti yazacaktir 
            
            self.miss_word += ' '
            #Kullaniciya daha iyi deneyim sunmak icin _ isaretini daha belirgin hale getirmeyi amaclar
            
        #Burada self.orj_word ile baslangicta rastgele uretilen kelimeyi kullanarak (for dongusunde)
        #for da her bir harfi alip if else komutuna bağlı olarak ms_word_old'a ekliyoruz
        #Bu ekleme islemi kullanicinin harfi dogru tahmin edip etmemesine gore oyun alanini yenileyecektir
        
        if ct and prev_size_dDC == len(list(self.deletiDictC)):
            result_mes,cont = (self.messages_which_is_per_step_of_game('Wrong'),False if l not in self.deletiDictC 
                  else self.messages_which_is_per_step_of_game('Already guessed'),False)
        #Burada ise for dongusunun basinda bahsettigimiz sekilde boyut karsilastirmasi yapar
        #Ekstra olarak oyun basini ile ortasini karistirmamasi icin ct adli bir kontrol degiskeni kullandik
        #self.Message_Ins_o_Gm() fonskiyonu ise if else kontrolu altinda oyun ici gelismelere gore mesaj gonderir

        print(self.miss_word.rstrip())
        #Burada ise sonuc tabloyu yazdiracagiz
        #.rstrip() yapmamizin sebebi tablonun en sagdan olusacak boslugu temizlemektir
        
        return result_mes,cont if ct else None,None
        #Burada ise user_space de kontrol etmek icin degiskenleri geri yollayacagiz
        #else in sebebi yine bahsettigimiz gibi ct nin False olma olasiligina bagli olarak
    def messages_which_is_per_step_of_game(self,gım):
        if gım == 'Wrong':
            return "Girdiğiniz harf bahsedilen kelime de bulunmamaktadır"
        elif gım == 'Correct':
            return "Girdiğiniz Harf doğrudur tebrikler"
        elif gım == 'Already guessed':
            return "Girdiğini harf önceden kullanılmıştır"
        
        #Burada kelimelerin dogru oldugunu , yanlis oldugunu ve onceden kullanilip kullanimaldigini belirten mesajlar vardir 
    def is_new_correct_letter(self,lets):
        """   
              Burada biz kullanıcının son söylediği doğru harfi gösteriyoruz
                                                                          """
        self.deletiDictC.add(lets)
        #Burada eger harf dogruysa harfi dogru bulunan harfler kumesine atiyoruz
        return f"{lets}"
        #Burada create_space_of_game_for_random_word fonksiyonun da kullanicinin yeni girdigi harf dogru oldugu icin bu harfi yazdiracak harfi geri dondurecek  
    def using_section(self):
        """
              Bu alanda kullanıcıya harf tahmin etmesi veya 
              kelime tahmin etmesi için standart bir menü işlemi yapılacak
                                                                         """
        cont,opt = True,None
        #Burada degiskenlerden cont degiskeni while dongusu icerisinde kullanici dogru islemi yaparsa cikis islemi saglayacaktir
        #opt degiskeni ise kullanicinin girdigi deger eger secenek 1 veya 2 ye esit olup olmadigini kontrol edecek
        while cont:
            
            try:
                opt = str(input("""Kelime Tahmininde bulunmak istiyorsanız 1
                                Harf Tahmininde bulunmak istiyorsanız 2 ye basınız : """))
                opt = opt.lstrip(' ')
                #Burada kullanicdan uygun secenegi istiyoruz
                #.lstrip() ile kullanicin soldan biraktigi bosluklari sorun cikartmasin diye siliyoruz
                               
                if not (opt == '1' or opt == '2'):
                    raise ValueError("Girdiginiz ifade seçenekleri karşılamamaktadır ")
                #Eger secenekler uyusmazsa hata mesajini verecegiz ve try except yapisindan cikip islemi tekrar edecegiz
                cont = False
                #while dongusunden cikis komutu
                
            except ValueError as e:
                print(f"Hata Mesajı : {e}")
            #try except yapisi ile kullanicin yanlis hareketini olma olasiligindan dolayi kontrol ediyoruz 
            
        return opt
        #kullanicinin girdigi deger esit ise user_space (main Function) a geri dondurecektir 
    def guessing_word(self):
        """
              Bu alan kullanıcının kelime tahmini yapabilmesi için kullanılacaktır
                                                                                 """
        def is_there_letters(w):
         
            for i in w:
                if i not in self.letters:
                    return False
                #Eger i elemanı bir harf degilse geriye False dondurecektir
            return True
            #Eger tum i elemanları birer harf ise kelime oldugunu kabul et ve kullaniciya onay ver
            
        #is_there_letters fonksiyonu kullanicin girdigi girdinin bir kelime ozelligi tasiyip tasimadigini kontrol edecektir
        
        cont,word = True,None
        #Burada cont while dongusunden cikisi kontrol edecektir
        #word kullanicin girdigi kelimeyi tutacaktir (tahmini degeri)
        
        while cont:
            word = str(input("Lütfen tahmin ettiğiniz kelimeyi giriniz")).upper().strip()
            #Kullanicidan tahmini kelimeyi alacaktir
            #Dogru ve gurultusuz veri icin hem yanlardaki bosluklari temizlenecektir hem de verilerin tum harfleri buyuk oldugundan donusturulecektir
            try:
                if (is_there_letters(word) if len(word) != 0 else True):
                    raise ValueError("Girdiğiniz tahmin bir kelime değildir")
                #Burada 2 katmanli bir dogrulama bulunacaktir
                #Ilk katman girilen bir seyin kesinlikle yazilmis olmasi lazimdir yoksa hata mesajina dondurulecektir
                #Ikinci katman da ise kelimenin icindeki her bir terimin harf olup olmadigini kontrol edilecektir
                #Bu katmanlardan birisi True dondurse bile try except yapisindan cikarilip kullanicidan yeni kelime istenilecektir
                cont = False
                #cont False olunca while dongusunden cikilmis olacaktir
            except ValueError as e:
                print(f"Hata Mesajı : {e}")
            #try except yapisi ile kullanicin yanlis hareketini olma olasiligindan dolayi kontrol ediyoruz     
        
        if word == self.orj_word:
            self.create_if_guessing_word_is_right()
            #Bu fonksiyon kelime dogru oldugunu gostermesi icin cizdirme islemi yaptiracaktir
        
            return "Girdiğiniz kelime doğrudur" , True
        else:
            return "Girdiğiniz kelime yanlıştır" , False
        #Burada eger kelime orijinal kelimeyle uyumlu ise Kelimenin dogrulugu oldugunu soyleyecektir degilse de tam tersini gosterecek
        #user_space alanında oyunu sonlandırma kosulunu saglamak icin ekstra olarak True degerini dondurecektir
        #user_space alanında oyunu devam ettirme kosulunu saglamak icin ekstra olarak False degerini dondurecektir
        
    def create_if_guessing_word_is_right(self):
        """   
              Burada kullanicinin kelimeyi dogru bulmasi kosuluna bagli 
              olarak Kelimeyi yazdirma islemi yaptirilacaktir
                                                            """
        for let in self.orj_word:
            
            self.miss_word += (let,' ')
            #Burada ise aldigimiz tum harfleri self.orj_word a gore self.miss_word uzerine ekliyoruz
            #Bosluk eklememizin sebebi harflerin belirgin konumlarda bulunması gerektigidir
            
        #Burada for dongusu ile orijinal kelimenin tum harflerini yazdirmak icin aliyoruz
        
        print(self.miss_word.rstrip())
        #Burada self.miss_word'u sagdan ekledigimiz ekstra bosluk silecek sekilde yazdiriyoruz
        
        self.begin_of_game()
        #Bellek gereksiz veri kalmasin diye self.miss_word kelimesini sifirliyoruz 
        
    def guessing_letter(self):
        """
              Kullanıcının kelimeyi bulmak icin harf tahmini yaptigi alandir
                                                                         """
        def is_there_letter(l):
            if l not in self.table:
                return True
            #Burada harfin eger self.table bulunmamasi kosulunu sagliyorsa geriye True dondureceginden bahsediyor
            #Bu True guessing_letter fonksiyonunda try excepte hata fonksiyonunu tetiklemektedir
            
            self.all_deli_Dict.add(l)
            #Burada self.all_deli_Dict fonksiyonun da kullanicinin girdigi harf dogru da olsa yanlis da olsa eklenmesini istiyoruz
            
            self.table.remove(l)
            #Ana tablodan elemanı cikartiriz ki kullanicini bir daha aynı harfi girerse function ayni islemlere takilmasin
            
            print("Yeni tablo : " , self.table)
            return False
            #Burada yeni tabloyu kullaniciya sunuyoruz ve try except te ki hata fonksiyonunda cikmak icin geriye False donduruyoruz
            
        #Bu fonksiyonunda kullanicinin yeni girdigi harfin onceden kullanilip kullanilmadigi kontrol edilecektir
        #Ona gore eger harf yeniyse ana tablodan silme islemi yapilacaktir
        
        cont = True
        #cont degiskeni burada while dongusunu kontrol edecektir
        while cont:
            letter = str(input("Lütfen tahmin ettiğiniz harfi giriniz")).upper().strip()
            #Burada kullanicidan tahmin etmesini istedigi harfi istiyoruz
            #Gurultuyu engellemek icin harfleri Verilerden dolayi buyuk harfe ceviriyoruz ve yanlardaki harfleri degistiriyoruz
            
            try:
                if (is_there_letter(letter) if len(letter) != 0 else True):
                    raise ValueError("Girdiğiniz ifade bir harf değildir")
                #Burada 2 katmanli bir dogrulama bulunacaktir
                #Ilk katman girilen bir seyin kesinlikle yazilmis olmasi lazimdir yoksa hata mesajina dondurulecektir
                #Ikinci katman da ise kelimenin icindeki her bir terimin harf olup olmadigini kontrol edilecektir
                #Bu katmanlardan birisi True dondurse bile try except yapisindan cikarilip kullanicidan yeni kelime istenilecektir
                cont = False
                #Burada while dongusunden cikmak icin cont degiskeninin degerini False'a ceviriyoruz 
                
            except ValueError as e:
                print("Hata mesajı : {}".format(e))
            #try except yapisi ile kullanicin yanlis hareketini olma olasiligindan dolayi kontrol ediyoruz     
        
        return self.create_space_of_game_for_random_word(letter,True)
        #Burada kullaniciya oyun alanina guncel halini gorebilmesi icin self.create_space_of_game_for_random_word fonksiyonuna gonderiyoruz
        #True da gondermemizin sebebi Oyun alaninin oyunun yeniden baslatildigi yanilsamasina dusmemesi icindir
        #Ve self.create_space_of_game_for_random_word den aldıgımız 2 degiskeni user_space fonksiyonuna geri donduruyoruz
    def create_random_word(self,idx):
        """
              Burada kullanıcının seçtiği türe göre rastgele eleman oluşturur
                                                                           """
        category = self.df.columns[idx]
        #Burada category'e sayisal degiskenin karsilik geldigi column degerini giriyoruz
        
        random_index = rd.randint(0, len(self.df[category]) - 1)
        #Burada rastgele bir eleman secilecegi icin o elemana ait bir random_index secilir
        
        self.orj_word = str(self.df.at[random_index,category]).upper()
        #Burada self.df uzerinden index numarasi ve column'a gore tablodan bir eleman olusturacagiz
        #Gurultuden uzaklasmasi icin ve akici bir gosterim olmasi icin harfleri buyuk harf yapacagiz
        
    def objects(self):     
        """ 
              Bu alanda kullanıcıya seçebileceği konu başlıklarını gösteriyoruz
                                                                           """                     
        return """ Aşağıda verilen konulardan istediğiniz birisinin numarasına göre giriş yapınız 
        1 -> Sehirler
        2 -> Filmler
        3 -> Hayvanlar
        4 -> Meslekler
        5 -> Bitkiler   """
    #Burada kullaniciya ozel geri bildirim mesajini geri donduruyoruz
    def choose_type_of_word(self):
        """
              Bu alanda kullanıcının hangi türü seçmek istediği istenir
                                                                   """
        def read_the_file():
            try:    
                self.df = pd.read_excel(r"Hang_man_DataBase.xlsx")
                #Burada dosyayi okuyoruz
                
            except FileNotFoundError:
                print("Hata mesajı : Dosya bulunamadı !!! ")
                sys.exit()
                #Burada dosya bulunamadiysa hata verdiriyoruz ve cikis yapiyoruz
                
            except Exception:
                print("Hata mesajı : Dosya okurken hata oluştu !!!")
                sys.exit()
                #Burada dosya okunurken bir hata olustuysa hata veriyoruz ve cikis yapiyoruz
                
        #read_the_file fonksiyonunda dosya saglam mi ya da kullanilabilir mi onu kontrol edecegiz
        
        print(self.objects())
        #Burada kullanicinin secebilecegi secenekleri gosteriyoruz
        
        read_the_file()
        #Burada dosyanin calisip calismadigini kontrol ediyoruz calisiyorsa self.df icerisine dosya da ki veri setini atıyoruz
        
        cont,sort = True,None
        #cont while dongusunden cikisi kontrol edecek
        #sort kullanicinin girdigi degeri alir
        
        while cont:
            sort = str(input("Lütfen Bahsedilen seçeneklerden birisini giriniz : ")).strip()
            #Burada kullaniciya soz edilen seceneklerden birisini girmesi istenir
            #.strip() ile sagdan ve soldan bosluklar temizlenir
            
            try:
                if sort not in {'1','2','3','4','5'}:
                    raise ValueError("Boyle bir seçenek türü bulunmamaktadır")
                #Burada kullanicinin girdigi degerin gercekten secenek olup olmadigi kontrol edilir
                #Eger degilse hata mesaji yazdirir
                cont = False
                #cont = False donguden while donguden cikmamizi saglar
                
            except ValueError as e:
                print(f"Hata Mesajı : {e}")
            #try except yapisi ile kullanicin yanlis hareketini olma olasiligindan dolayi kontrol ediyoruz
        
        return int(sort) -1
        #Buradan rastgele kelime secen fonksiyona kategorinin indexini donderiyoruz
        
    def user_space(self):
        """
              Bu alan bizim Ana fonksiyonumuz olacaktır Burada Oyun tablosu olusturma, 
              oyun alanini kullanmadan once cizim yapilmasi icin self.miss_word degerini
              olusturuyoruz ve belirli iterasyonlara bagli olacak kontrol sistemini insa 
              ediyoruz ve kullaniciya rastgele kelimenin turunu secmesi icin bir alana 
              yonlendiriyoruz son olarakta kullanici oyundan cikmak istiyorsa Exit fonksiyonu ile 
              sistemi sonlandiriyoruz        
                                       """
        def _exit():
            sys.exit()
            #Bu cikis direk sistemden olacagi icin sys kutuphanesi kullanacagiz
            
        #Sistemden cikmak icin bu fonksiyonu kullanacagiz
        
        print("""Oyuna Hoşgeldiniz
        Lütfen bekleyiniz ... """)
        t.sleep(3)
        #Burada Kullaniciya karsilama yapip 3 saniye bekletiyoruz
        
        hak,pck = 0,None
        #Burada kullanicinin yaptigi yanlis hamleye bagli olarak hak sayisi olacaktir
        #Ve kullanicinin harf tahmin veya kelime tahmin isteyecegi alanda kullanilacak pck degiskeni olacaktir
        
        idx = self.choose_type_of_word()
        #Buradan kullanicinin hangi kategoriyi secmek istedigini soruyoruz
        
        self.create_random_word(idx)
        #Sonucunda da kategoriye bagli rastgele kelime seciyoruz
        
        self.begin_of_game()
        #Burada oyun alanı icin self.miss_word degiskenini olusturuyoruz ya da sifirliyoruz
        
        text,tri = self.create_space_of_game_for_random_word(None, False)
        #Burada kullanici oyuna baslamadan once cikan kelimenin gosterilecegi alana yonlendiriyoruz
        #text,tri ye atama yapmamizin sebebi self.create_space_of_game_for_random_word fonksiyonun da geri dondurme islemi yapmamiz
        
        self.table = self.copy_of_letters_table()
        #Burada ise ana tabloyu sıfırlamamak icin kullabilecegimiz kopya bir tablo olusturacagiz
        
        while hak != 5:
            pck = self.using_section()
            #Burada kullanicidan Kelime tahmini veya Harf tahmini icin bir menu alanına yonlendirip kullanicinin secimini alacagiz
            
            control = lambda pck:self.guessing_word() if pck == '1' else self.guessing_letter()
            text,tri= control(pck)
            #Burada ise lambda ile kullanicinin secimine gore fonksiyonlara atayacagiz 
            #Ve ciktilari almak icin control adli bir fonksiyon olusturacagiz
            #Bu ciktilar dan text kullanicinin hamlesine bagli olarak geri mesaj gonderecektir
            #tri ise 2 isleme yarayacaktir
            #tri nin 1. islemi : eger kelime tahmini dogru ise (pck == '1' icin ) oyunu bittiginden bahsedecektir ve donguden cikacaktir
            #tri nin 2. islemi : eger kullanicinin gerek self.guessing_word() gerekse self.guessing_letter() fonksiyondan aldigi sonuca bagli olarak 
            #tri nin 2. islem (devami) : hak degerini yukseltecek ve adami cizdirecektir
            #tri lerde yapilan break komutu kosula bagli olarak cikis islemini saglayacaktir
                
            print(text)
            #Burada kullanicinin hamlesine bagli olarak geri gelen mesaji yazdiracaktir
            
            if pck == '1' and tri:
                print(self.message_end_of_game(hak))
                break
            #tri islem - 1 icin olan kisim 
            
            if not tri:
                hak += 1
                print(self.drawing_man(hak))
            #tri islem -2 icin olan kisim
            
            if '_' not in self.miss_word:
                print(self.message_end_of_game(hak))
                break
            #Burada ise self.miss_word olusturduktan sonra icerisinde oyun alaninda kullanacagimiz bolumun icinde _ var mı yok mu kontrol edecegiz
            
            self.begin_of_game()
            #Buradan tabloyu sifirlayacagiz 
            
            print(f'''Kalan harfler : {",".join(self.table)}
                  Kullanılan Harfler : {",".join(self.all_deli_Dict)}
                  Kalan Hak : {5 - hak}''')
            #Burada yaptigimiz sey ise kullaniciya kalan harfler kullanilan harfler ve kalan hakkini gostermektir       
            
        if hak == 5:
            print(self.message_end_of_game(hak))
        #Burada eger hak == 5 ise self.messegae_end_of_game() secenegine gonderilecek ve oyunu kaybettiniz mesaji verilecektir
        
        self.user_space() if self.process_end_of_game() else _exit()
        #Burada ise self.process_end_o_gm fonksiyonu ile kullaninicinin secimine bagli olarak oyuna yeniden baslayacaktir ya da Exit ile cıkıs yapacaktir
    def process_end_of_game(self):
        """
              Bu alanda kullanıcıya oyunun bittiğini söyleyip 
              yeniden başlaması veya oyundan çıkması icin secenek sunuyoruz
                                                                """
        l_ct = True
        #l_ct değişkeni bizim while dongumuzu kontrol edecektir 
        
        while l_ct:
             
            select_ls = str(input("""Oyun bitti ! 
                                  yeniden oynamak istiyorsanız 1
                                  istemiyorsanız ve çıkış yapmak istiyorsanız 2 ye tıklayınız: """)).strip()
            #Burada kullanici icin yeniden başlaması veya oyundan çıkması icin secenek sunuyoruz
            #ekstra olarak .strip() komutu ile bosluklardan dolayi olusabilecek gurultuyu engelliyoruz
            
            try:
                if select_ls not in ['1', '2']:
                    raise ValueError("Girdiğiniz seçenek oyun içinde bulunmamaktadır lütfen tekrar deneyiniz")
                #Burada select_ls diye bir secenek var mi diye kontrol ediyoruz
                l_ct = False
                #l_ct = False yaparak while dan disari cikiyoruz
                
            except ValueError as e:
                print(f"Hata mesajı : {e}")
            #try except yapisi ile kullanicin yanlis hareketini olma olasiligindan dolayi kontrol ediyoruz     
        return True if select_ls == '1' else False
        #Burada ise kullanicinin girdigi secenege baglı olarak Cikis ve yeniden oynamayi tetikleyen degeri geri donduruyoru
