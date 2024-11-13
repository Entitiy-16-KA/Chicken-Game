import tkinter as tk
from PIL import Image, ImageTk
import random

class ChickenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tavuk Oyunu")  # Başlık değiştirilmiştir

        # Pencere arkaplanı değişmedi
        self.root.configure(bg="white")  # Varsayılan arka plan rengi

        # Ekran boyutunu al ve biraz küçült (görev çubuğu için boşluk bırak)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight() - 50

        # Pencereyi boyutlandır ve ortala
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        # Canvas oluştur
        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Arka plan resmini yükle
        self.load_background_image()

        # Tavuk resmini yükle
        self.load_chicken_image()

        # Draco ve Draco atış resmini yükle
        self.load_draco_image()
        self.load_draco_shot_image()

        # Fox ve Fox atış resmini yükle (fox_shot.jpg ile)
        self.load_fox_image()
        self.load_fox_shot_image()

        # Tavuk resminin rastgele başlangıç konumu
        self.chicken_x = random.randint(self.chicken_width // 2, self.screen_width - self.chicken_width // 2)
        self.chicken_y = random.randint(self.chicken_height // 2, self.screen_height - self.chicken_height // 2)
        self.chicken = self.canvas.create_image(self.chicken_x, self.chicken_y, image=self.chicken_image)

        # Draco ve Fox'un rastgele spawnlanması
        self.dracos = []  # Draco resimlerinin listesi
        self.foxes = []  # Fox resimlerinin listesi
        self.draco_shots = []  # Draco mermilerinin listesi
        self.fox_shots = []  # Fox mermilerinin listesi
        self.spawn_draco()  # Başlangıçta bir Draco ekle
        self.spawn_fox()    # Başlangıçta bir Fox ekle

        # Basılı tuşları saklamak için bir küme
        self.pressed_keys = set()

        # Klavye ok tuşlarını bağlama
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        # Hareket işlevini sürekli çağırarak animasyonu başlat
        self.update_position()

    def load_background_image(self):
        """Arka plan resmini yükle ve canvas'a yerleştir."""
        image = Image.open("arka_plan.jpg")
        image = image.resize((self.screen_width, self.screen_height), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        # Arka planı canvas'a ekle
        self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)

    def load_chicken_image(self):
        # Resmi yükleyip yeniden boyutlandırma
        image = Image.open("chicken.png")
        image = image.resize((100, 100), Image.LANCZOS)
        self.chicken_image = ImageTk.PhotoImage(image)

        # Resmin boyutunu sakla
        self.chicken_width = image.width
        self.chicken_height = image.height

    def load_draco_image(self):
        # Draco'nun resmini yükle
        draco_image = Image.open("draco.png")
        draco_image = draco_image.resize((100, 100), Image.LANCZOS)
        self.draco_image = ImageTk.PhotoImage(draco_image)

        # Draco'nun boyutunu sakla
        self.draco_width = draco_image.width
        self.draco_height = draco_image.height

    def load_draco_shot_image(self):
        # Draco'nun atış resmini yükle, mermiyi biraz küçült
        shot_image = Image.open("draco_shot.png")
        shot_image = shot_image.resize((35, 35), Image.LANCZOS)  # Mermiyi küçültüyoruz
        self.draco_shot_image = ImageTk.PhotoImage(shot_image)

        # Merminin boyutunu sakla
        self.draco_shot_width = shot_image.width
        self.draco_shot_height = shot_image.height

    def load_fox_image(self):
        # Fox'un resmini yükle
        fox_image = Image.open("fox.png")
        fox_image = fox_image.resize((100, 100), Image.LANCZOS)
        self.fox_image = ImageTk.PhotoImage(fox_image)

        # Fox'un boyutunu sakla
        self.fox_width = fox_image.width
        self.fox_height = fox_image.height

    def load_fox_shot_image(self):
        # Fox'un atış resmini yükle (şimdi fox_shot.jpg)
        fox_shot_image = Image.open("fox_shot.jpg")
        fox_shot_image = fox_shot_image.resize((35, 35), Image.LANCZOS)
        self.fox_shot_image = ImageTk.PhotoImage(fox_shot_image)

        # Merminin boyutunu sakla
        self.fox_shot_width = fox_shot_image.width
        self.fox_shot_height = fox_shot_image.height

    def spawn_draco(self):
        """Draco resmini sol kenarda rastgele bir yükseklikte spawnlar."""
        draco_x = 50  # Sol kenarda sabit
        draco_y = random.randint(self.draco_height // 2, self.screen_height - self.draco_height // 2)
        draco = self.canvas.create_image(draco_x, draco_y, image=self.draco_image)
        self.dracos.append(draco)

        # Draco'nun atışını başlat
        self.shoot_draco(draco)

        # Her 1000 milisaniyede bir yeni Draco ekle
        self.root.after(1000, self.spawn_draco)

    def shoot_draco(self, draco):
        """Draco'nun atışını başlat."""
        draco_x, draco_y = self.canvas.coords(draco)
        shot = self.canvas.create_image(draco_x + self.draco_width, draco_y, image=self.draco_shot_image)
        self.draco_shots.append(shot)

        # Mermiyi hareket ettir
        self.move_draco_shot(shot)

    def move_draco_shot(self, shot):
        """Mermiyi hareket ettir."""
        shot_x, shot_y = self.canvas.coords(shot)
        new_shot_x = shot_x + 15  # Mermi her hareket ettiğinde 15px ileri gider (hız arttı)

        # Mermi ekranın dışına çıkarsa, onu sil
        if new_shot_x > self.screen_width:
            self.canvas.delete(shot)
            self.draco_shots.remove(shot)
        else:
            self.canvas.coords(shot, new_shot_x, shot_y)
            self.check_collision(shot)  # Çarpışma kontrolü

        # Mermiyi sürekli olarak hareket ettir
        self.root.after(20, self.move_draco_shot, shot)  # Daha hızlı ve pürüzsüz hareket

    def spawn_fox(self):
        """Fox resmini sol kenarda rastgele bir yükseklikte spawnlar."""
        fox_x = 50  # Sol kenarda sabit
        fox_y = random.randint(self.fox_height // 2, self.screen_height - self.fox_height // 2)
        fox = self.canvas.create_image(fox_x, fox_y, image=self.fox_image)
        self.foxes.append(fox)

        # Fox'un atışını başlat
        self.shoot_fox(fox)

        # Her 1500 milisaniyede bir yeni Fox ekle (Draco'dan biraz daha geç)
        self.root.after(1500, self.spawn_fox)

    def shoot_fox(self, fox):
        """Fox'un atışını başlat."""
        fox_x, fox_y = self.canvas.coords(fox)
        shot = self.canvas.create_image(fox_x + self.fox_width, fox_y, image=self.fox_shot_image)
        self.fox_shots.append(shot)

        # Mermiyi hareket ettir
        self.move_fox_shot(shot)

    def move_fox_shot(self, shot):
        """Fox'un mermisini hareket ettir."""
        shot_x, shot_y = self.canvas.coords(shot)
        new_shot_x = shot_x + 10  # Fox'un mermisi biraz daha yavaş hareket eder

        # Mermi ekranın dışına çıkarsa, onu sil
        if new_shot_x > self.screen_width:
            self.canvas.delete(shot)
            self.fox_shots.remove(shot)
        else:
            self.canvas.coords(shot, new_shot_x, shot_y)
            self.check_collision(shot)  # Çarpışma kontrolü

        # Mermiyi sürekli olarak hareket ettir
        self.root.after(20, self.move_fox_shot, shot)  # Daha hızlı ve pürüzsüz hareket

    def check_collision(self, shot):
        """Mermilerin tavukla çarpışıp çarpmadığını kontrol et."""
        shot_x, shot_y = self.canvas.coords(shot)

        # Tavuk ve mermi arasındaki çarpışmayı kontrol et
        chicken_x, chicken_y = self.canvas.coords(self.chicken)
        if (shot_x > chicken_x - self.chicken_width // 2 and shot_x < chicken_x + self.chicken_width // 2 and
            shot_y > chicken_y - self.chicken_height // 2 and shot_y < chicken_y + self.chicken_height // 2):
            self.reset_game()

    def reset_game(self):
        """Oyunu sıfırla ve başlangıç durumuna getir."""
        self.canvas.delete("all")  # Ekrandaki tüm öğeleri temizle
        self.__init__(self.root)  # Yeniden başlat

    def on_key_press(self, event):
        # Basılan tuşu küme içine ekle
        self.pressed_keys.add(event.keysym)

    def on_key_release(self, event):
        # Bırakılan tuşu kümeden çıkar
        self.pressed_keys.discard(event.keysym)

    def update_position(self):
        # Hareket yönlerini sıfırla
        move_x, move_y = 0, 0

        # Basılı tuşlara göre hareket belirle
        if "Up" in self.pressed_keys:
            move_y = -20  # Hız arttı, 10'dan 20'ye
        if "Down" in self.pressed_keys:
            move_y = 20  # Hız arttı, 10'dan 20'ye
        if "Left" in self.pressed_keys:
            move_x = -20  # Hız arttı, 10'dan 20'ye
        if "Right" in self.pressed_keys:
            move_x = 20  # Hız arttı, 10'dan 20'ye

        # Yeni pozisyonu hesapla
        new_x = self.chicken_x + move_x
        new_y = self.chicken_y + move_y

        # Tavuk resminin ekranın dışına çıkmaması için sınır kontrolü
        if new_x >= self.chicken_width // 2 and new_x <= self.screen_width - self.chicken_width // 2:
            self.chicken_x = new_x

        if new_y >= self.chicken_height // 2 and new_y <= self.screen_height - self.chicken_height // 2:
            self.chicken_y = new_y

        # Tavuk resminin pozisyonunu güncelle
        self.canvas.coords(self.chicken, self.chicken_x, self.chicken_y)

        # Draco ve Fox resimlerinin pozisyonlarını kontrol et, hareket etmelerini engelle
        for draco in self.dracos:
            self.canvas.coords(draco, 50, self.canvas.coords(draco)[1])

        for fox in self.foxes:
            self.canvas.coords(fox, 50, self.canvas.coords(fox)[1])

        # Bu işlevi tekrar çağırarak sürekli hareket sağlar
        self.root.after(20, self.update_position)

# Ana pencereyi oluşturma
root = tk.Tk()
app = ChickenApp(root)
root.mainloop()
