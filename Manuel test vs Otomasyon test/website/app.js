// NovaStore - E-Ticaret Uygulama Mantığı

(function () {
  'use strict';

  // Durum Yönetimi
  const state = {
    cart: [],
    coupon: null,
    discountRate: 0.10, // %10 indirim
    validCoupon: 'INDIRIM10',
    currentUser: null,
    validUser: {
      email: 'arda@gmail.com',
      password: 'arda123',
      name: 'Arda'
    }
  };

  // DOM Elementleri
  const elements = {
    // Navigasyon & Butonlar
    openLoginBtn: document.getElementById('openLoginBtn'),
    userBtnText: document.getElementById('userBtnText'),
    cartBtn: document.getElementById('cartBtn'),
    cartBadge: document.getElementById('cartBadge'),

    // Sepet Drawer
    cartModal: document.getElementById('cartModal'),
    closeCartBtn: document.getElementById('closeCartBtn'),
    emptyCart: document.getElementById('emptyCart'),
    cartItems: document.getElementById('cartItems'),
    couponCodeInput: document.getElementById('couponCodeInput'),
    applyCouponBtn: document.getElementById('applyCouponBtn'),
    couponStatus: document.getElementById('couponStatus'),
    subtotalText: document.getElementById('subtotalText'),
    discountRow: document.getElementById('discountRow'),
    discountText: document.getElementById('discountText'),
    totalText: document.getElementById('totalText'),
    checkoutBtn: document.getElementById('checkoutBtn'),

    // Giriş Modalı
    loginModal: document.getElementById('loginModal'),
    closeLoginBtn: document.getElementById('closeLoginBtn'),
    loginForm: document.getElementById('loginForm'),
    loginEmail: document.getElementById('loginEmail'),
    loginPassword: document.getElementById('loginPassword'),
    emailError: document.getElementById('emailError'),
    passwordError: document.getElementById('passwordError'),
    loginAlert: document.getElementById('loginAlert'),
    submitLoginBtn: document.getElementById('submitLoginBtn'),
    loginHint: document.getElementById('loginHint'),

    // Başarılı Sipariş Modalı
    orderSuccessModal: document.getElementById('orderSuccessModal'),
    closeSuccessBtn: document.getElementById('closeSuccessBtn'),

    // Toast
    toast: document.getElementById('toast')
  };

  function showToast(msg) {
    elements.toast.textContent = msg;
    elements.toast.className = 'toast show';
    setTimeout(() => {
      elements.toast.className = 'toast';
    }, 2500);
  }

  function formatMoney(amount) {
    return amount.toLocaleString('tr-TR') + ' TL';
  }

  // ==============================
  // GİRİŞ YAP İŞLEMLERİ
  // ==============================
  function openLogin() {
    if (state.currentUser) {
      state.currentUser = null;
      elements.userBtnText.textContent = 'Giriş Yap';
      showToast('Oturum kapatıldı.');
      return;
    }
    clearLoginErrors();
    elements.loginModal.classList.add('active');
  }

  function closeLogin() {
    elements.loginModal.classList.remove('active');
  }

  function clearLoginErrors() {
    elements.emailError.textContent = '';
    elements.passwordError.textContent = '';
    elements.loginAlert.style.display = 'none';
    elements.loginEmail.classList.remove('error');
    elements.loginPassword.classList.remove('error');
  }

  elements.openLoginBtn.addEventListener('click', openLogin);
  elements.closeLoginBtn.addEventListener('click', closeLogin);

  // İpucuna tıklayınca otomatik doldurma (kolaylık için)
  if (elements.loginHint) {
    elements.loginHint.addEventListener('click', () => {
      elements.loginEmail.value = 'arda@gmail.com';
      elements.loginPassword.value = 'arda123';
      clearLoginErrors();
    });
  }

  function handleLogin(e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    clearLoginErrors();

    const rawEmail = elements.loginEmail.value.trim();
    const cleanEmail = rawEmail.toLowerCase();
    const rawPassword = elements.loginPassword.value.trim();
    let hasError = false;

    // Boş alan kontrolü
    if (!rawEmail) {
      elements.emailError.textContent = 'E-posta adresi boş bırakılamaz.';
      elements.loginEmail.classList.add('error');
      hasError = true;
    }

    if (!rawPassword) {
      elements.passwordError.textContent = 'Şifre alanı boş bırakılamaz.';
      elements.loginPassword.classList.add('error');
      hasError = true;
    }

    if (hasError) return false;

    // Hem 'arda@gmail.com' hem de sadece 'arda' yazılırsa kabul et
    const isEmailValid = (cleanEmail === 'arda@gmail.com' || cleanEmail === 'arda');
    const isPassValid = (rawPassword === 'arda123');

    // Kimlik kontrolü
    if (isEmailValid && isPassValid) {
      state.currentUser = state.validUser;
      elements.userBtnText.textContent = 'Hesabım (Arda)';
      closeLogin();
      showToast('Giriş başarılı! Hoş geldiniz Arda.');
      return true;
    } else {
      elements.loginAlert.textContent = 'Hatalı e-posta veya şifre girdiniz!';
      elements.loginAlert.className = 'alert error';
      elements.loginAlert.style.display = 'block';
      return false;
    }
  }

  elements.loginForm.addEventListener('submit', handleLogin);
  elements.submitLoginBtn.addEventListener('click', handleLogin);

  // ==============================
  // SEPET İŞLEMLERİ
  // ==============================
  function openCart() {
    elements.cartModal.classList.add('active');
  }

  function closeCart() {
    elements.cartModal.classList.remove('active');
  }

  elements.cartBtn.addEventListener('click', openCart);
  elements.closeCartBtn.addEventListener('click', closeCart);

  // Ürün Ekle Butonları
  document.querySelectorAll('.btn-add').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = parseInt(btn.getAttribute('data-id'), 10);
      const name = btn.getAttribute('data-name');
      const price = parseFloat(btn.getAttribute('data-price'));

      addToCart(id, name, price);
    });
  });

  function addToCart(id, name, price) {
    const existing = state.cart.find(item => item.id === id);
    if (existing) {
      existing.qty += 1;
    } else {
      state.cart.push({ id, name, price, qty: 1 });
    }

    updateCartUI();
    showToast(`"${name}" sepete eklendi!`);
  }

  window.removeFromCart = function (id) {
    state.cart = state.cart.filter(item => item.id !== id);
    updateCartUI();
  };

  function updateCartUI() {
    // Badge
    const totalItems = state.cart.reduce((sum, item) => sum + item.qty, 0);
    elements.cartBadge.textContent = totalItems;

    // Liste
    if (state.cart.length === 0) {
      elements.emptyCart.style.display = 'block';
      elements.cartItems.innerHTML = '';
      elements.checkoutBtn.disabled = true;
      elements.subtotalText.textContent = '0 TL';
      elements.totalText.textContent = '0 TL';
      elements.discountRow.style.display = 'none';
      return;
    }

    elements.emptyCart.style.display = 'none';
    elements.checkoutBtn.disabled = false;

    elements.cartItems.innerHTML = state.cart.map(item => `
      <div class="cart-item">
        <div class="cart-item-info">
          <strong>${item.name}</strong>
          <span>${formatMoney(item.price)} x ${item.qty} Adet</span>
        </div>
        <button class="btn-del" onclick="removeFromCart(${item.id})">Kaldır</button>
      </div>
    `).join('');

    // Fiyat Hesaplama
    const subtotal = state.cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
    elements.subtotalText.textContent = formatMoney(subtotal);

    let discount = 0;
    if (state.coupon === state.validCoupon) {
      discount = subtotal * state.discountRate;
      elements.discountRow.style.display = 'flex';
      elements.discountText.textContent = '-' + formatMoney(discount);
    } else {
      elements.discountRow.style.display = 'none';
    }

    const total = subtotal - discount;
    elements.totalText.textContent = formatMoney(total);
  }

  // Kupon Uygula
  elements.applyCouponBtn.addEventListener('click', () => {
    const code = elements.couponCodeInput.value.trim().toUpperCase();

    if (code === state.validCoupon) {
      state.coupon = code;
      elements.couponStatus.textContent = '✓ %10 İndirim kuponu uygulandı!';
      elements.couponStatus.className = 'coupon-msg success';
      showToast('Kupon uygulandı!');
    } else {
      state.coupon = null;
      elements.couponStatus.textContent = '❌ Geçersiz kupon kodu.';
      elements.couponStatus.className = 'coupon-msg error';
    }

    updateCartUI();
  });

  // Sipariş Tamamla
  elements.checkoutBtn.addEventListener('click', () => {
    if (state.cart.length === 0) return;
    closeCart();
    elements.orderSuccessModal.classList.add('active');
    // Sepeti sıfırla
    state.cart = [];
    state.coupon = null;
    elements.couponCodeInput.value = '';
    elements.couponStatus.textContent = '';
    updateCartUI();
  });

  elements.closeSuccessBtn.addEventListener('click', () => {
    elements.orderSuccessModal.classList.remove('active');
  });

  // Dışarı tıklayınca kapatma
  window.addEventListener('click', (e) => {
    if (e.target === elements.cartModal) closeCart();
    if (e.target === elements.loginModal) closeLogin();
    if (e.target === elements.orderSuccessModal) elements.orderSuccessModal.classList.remove('active');
  });

  // İlk başlatma
  updateCartUI();
})();
