"""
NovaStore - Otomasyon Test Senaryosu (Selenium WebDriver)
Ders Sunumu: Manuel Test vs Otomasyon Test
Süre: ~5-10 saniye (Sınıfta canlı izlenebilmesi için görsel adımlarla çalışır)
"""

import os
import sys
import time
from pathlib import Path

# Renkli terminal çıktıları için
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    GREEN = Fore.GREEN + Style.BRIGHT
    RED = Fore.RED + Style.BRIGHT
    CYAN = Fore.CYAN + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    GREEN = RED = CYAN = YELLOW = RESET = ""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

def print_banner():
    print(f"\n{CYAN}=" * 65)
    print(f"{CYAN}       NOVASTORE E-TİCARET OTOMASYON TESTİ (SELENIUM)")
    print(f"{CYAN}       Konu: Manuel Test vs Otomasyon Test Canlı Demosu")
    print(f"{CYAN}=" * 65 + f"{RESET}\n")

def highlight(driver, element, duration=0.4):
    """Sınıfın canlı görebilmesi için tıklanan/yazılan elementi sarı çerçeve ile parlatır."""
    try:
        driver.execute_script("arguments[0].style.outline = '3px solid #f59e0b';", element)
        time.sleep(duration)
        driver.execute_script("arguments[0].style.outline = '';", element)
    except Exception:
        pass

def get_driver():
    """Chrome veya Edge tarayıcısını otomatik başlatır."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--log-level=3")
    
    # Otomasyon bilgi çubuğunu gizle
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    try:
        # Önce Chrome dene
        return webdriver.Chrome(options=options)
    except Exception:
        # Chrome olmazsa Edge dene
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--log-level=3")
        return webdriver.Edge(options=edge_options)

def run_tests():
    print_banner()

    # Web sitesinin yerel dosya yolu (İnternet bağlantısına ihtiyaç duymaz)
    html_file = Path(__file__).parent / "website" / "index.html"
    file_url = html_file.resolve().as_uri()

    print(f"{YELLOW}[BİLGİ]{RESET} Tarayıcı başlatılıyor ve site açılıyor...")
    driver = get_driver()
    wait = WebDriverWait(driver, 10)

    start_total_time = time.time()
    passed_tests = 0
    total_tests = 5

    try:
        driver.get(file_url)
        time.sleep(1) # Sayfanın oturması için kısa bekleme

        # ========================================================
        # TEST 1: Negatif Giriş Testi (Boş Bırakılan Alan Kontrolü)
        # ========================================================
        t0 = time.time()
        print(f"\n{YELLOW}[TEST 1]{RESET} Negatif Giriş Testi (Boş Alan Validasyonu) yürütülüyor...")

        login_modal_btn = wait.until(EC.element_to_be_clickable((By.ID, "openLoginBtn")))
        highlight(driver, login_modal_btn)
        login_modal_btn.click()
        time.sleep(0.5)

        # Boş şekilde 'Giriş Yap' butonuna tıkla
        submit_btn = driver.find_element(By.ID, "submitLoginBtn")
        highlight(driver, submit_btn)
        submit_btn.click()
        time.sleep(0.5)

        # Hata mesajı çıktı mı kontrol et
        email_error = driver.find_element(By.ID, "emailError").text
        password_error = driver.find_element(By.ID, "passwordError").text

        assert "boş bırakılamaz" in email_error, "E-posta hata mesajı görüntülenmedi!"
        assert "boş bırakılamaz" in password_error, "Şifre hata mesajı görüntülenmedi!"

        t_elapsed = round(time.time() - t0, 2)
        print(f"         {GREEN}✓ BAŞARILI:{RESET} Boş alan uyarıları doğrulandı! ({t_elapsed} sn)")
        passed_tests += 1

        # ========================================================
        # TEST 2: Pozitif Giriş Testi (Doğru Kullanıcı Oturumu)
        # ========================================================
        t0 = time.time()
        print(f"\n{YELLOW}[TEST 2]{RESET} Pozitif Giriş Testi (Geçerli Kullanıcı Girişi)...")

        email_input = driver.find_element(By.ID, "loginEmail")
        password_input = driver.find_element(By.ID, "loginPassword")

        highlight(driver, email_input)
        email_input.send_keys("arda@gmail.com")
        time.sleep(0.4)

        highlight(driver, password_input)
        password_input.send_keys("arda123")
        time.sleep(0.4)

        highlight(driver, submit_btn)
        submit_btn.click()
        time.sleep(0.8)

        # Kullanıcı butonunda 'Hesabım (Arda)' yazıyor mu kontrol et
        user_btn_text = driver.find_element(By.ID, "userBtnText").text
        assert "Arda" in user_btn_text, f"Beklenen kullanıcı adı bulunamadı: {user_btn_text}"

        t_elapsed = round(time.time() - t0, 2)
        print(f"         {GREEN}✓ BAŞARILI:{RESET} Kullanıcı oturumu doğrulandı ({user_btn_text}) ({t_elapsed} sn)")
        passed_tests += 1

        # ========================================================
        # TEST 3: Sepete Ürün Ekleme (Fonksiyonel Test)
        # ========================================================
        t0 = time.time()
        print(f"\n{YELLOW}[TEST 3]{RESET} Sepete Ürün Ekleme Testi (Nova Sound Pro Kulaklık - 1.000 TL)...")

        add_btn = wait.until(EC.element_to_be_clickable((By.ID, "addToCartBtn1")))
        # Butona kaydır
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_btn)
        time.sleep(0.5)

        highlight(driver, add_btn)
        add_btn.click()
        time.sleep(0.6)

        # Sepet sayacının 1 olduğunu doğrula
        cart_badge = driver.find_element(By.ID, "cartBadge").text
        assert cart_badge == "1", f"Sepet adedi beklenen 1 yerine '{cart_badge}' geldi!"

        t_elapsed = round(time.time() - t0, 2)
        print(f"         {GREEN}✓ BAŞARILI:{RESET} Ürün sepete eklendi, sepet sayacı '1' oldu! ({t_elapsed} sn)")
        passed_tests += 1

        # ========================================================
        # TEST 4: Kupon Kodu & Fiyat Hesaplama (Matematiksel Doğrulama)
        # ========================================================
        t0 = time.time()
        print(f"\n{YELLOW}[TEST 4]{RESET} İndirim Kuponu Doğrulama ('INDIRIM10' -> %10 İndirim)...")

        # Sepeti aç
        cart_btn = driver.find_element(By.ID, "cartBtn")
        highlight(driver, cart_btn)
        cart_btn.click()
        time.sleep(0.6)

        # Kupon kodunu yaz
        coupon_input = wait.until(EC.visibility_of_element_located((By.ID, "couponCodeInput")))
        highlight(driver, coupon_input)
        coupon_input.send_keys("INDIRIM10")
        time.sleep(0.4)

        apply_coupon_btn = driver.find_element(By.ID, "applyCouponBtn")
        highlight(driver, apply_coupon_btn)
        apply_coupon_btn.click()
        time.sleep(0.6)

        # 1.000 TL'den %10 indirimle 900 TL'ye düşmesini kontrol et
        total_text = driver.find_element(By.ID, "totalText").text
        assert "900" in total_text, f"İndirim hesabı hatalı! Beklenen: 900 TL, Görünen: {total_text}"

        t_elapsed = round(time.time() - t0, 2)
        print(f"         {GREEN}✓ BAŞARILI:{RESET} Kupon uygulandı ve sepet 900 TL olarak doğrulandı! ({t_elapsed} sn)")
        passed_tests += 1

        # ========================================================
        # TEST 5: Sipariş Tamamlama
        # ========================================================
        t0 = time.time()
        print(f"\n{YELLOW}[TEST 5]{RESET} Siparişi Tamamlama Akışı Test Ediliyor...")

        checkout_btn = wait.until(EC.element_to_be_clickable((By.ID, "checkoutBtn")))
        highlight(driver, checkout_btn)
        checkout_btn.click()
        time.sleep(0.8)

        # Sipariş başarı modalı açıldı mı kontrol et
        success_modal = wait.until(EC.visibility_of_element_located((By.ID, "orderSuccessModal")))
        assert success_modal.is_displayed(), "Sipariş başarılı modalı açılmadı!"

        t_elapsed = round(time.time() - t0, 2)
        print(f"         {GREEN}✓ BAŞARILI:{RESET} Sipariş onay modalı başarıyla görüntülendi! ({t_elapsed} sn)")
        passed_tests += 1

        # Kapanış için 1.5 saniye bekle
        time.sleep(1.5)

    except AssertionError as ae:
        print(f"\n{RED}[TEST HATASI (FAIL)]:{RESET} {ae}")
    except Exception as e:
        print(f"\n{RED}[BEKLENMEYEN HATA]:{RESET} {e}")
    finally:
        total_time = round(time.time() - start_total_time, 2)
        driver.quit()

        # Özet Rapor Çıktısı
        print(f"\n{CYAN}=" * 65)
        print(f"{CYAN}                       TEST SONUÇ RAPORU")
        print(f"{CYAN}=" * 65)
        print(f" Toplam Koşulan Test  : {total_tests}")
        print(f" Başarılı Test (PASS) : {GREEN}{passed_tests}/{total_tests}{RESET}")
        print(f" Otomasyon Test Süresi: {GREEN}{total_time} saniye{RESET}")
        print(f" Manuel Test Süresi   : ~90 saniye (İnsan hızı tahmini)")
        print(f" Verimlilik Kazanımı  : {YELLOW}Yaklaşık {round(90 / max(total_time, 1), 1)} kat daha hızlı!{RESET}")
        print(f"{CYAN}=" * 65 + f"{RESET}\n")

if __name__ == "__main__":
    run_tests()
