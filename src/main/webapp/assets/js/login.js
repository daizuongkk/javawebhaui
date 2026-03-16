class SoftMinimalismLoginForm {
    constructor() {
        this.form = document.getElementById('loginForm');
        if (!this.form) return; // FIX: guard null trước khi dùng

        this.usernameInput = document.getElementById('username');
        this.emailInput = document.getElementById('email');
        this.passwordInput = document.getElementById('password');
        this.passwordConfirm = document.getElementById('passwordConfirm');
        this.passwordToggle = document.getElementById('passwordToggle');
        this.submitButton = this.form.querySelector('.comfort-button');
        this.successMessage = document.getElementById('successMessage');
        this.socialButtons = document.querySelectorAll('.social-soft');

        // FIX: guard chặn submit/social nhiều lần
        this._isSubmitting = false;
        this._socialLoading = new WeakMap();

        // FIX: lưu timer clearError để cancel khi cần
        this._clearErrorTimers = {};

        this.init();
    }

    init() {
        this.bindEvents();
        this.setupPasswordToggle();
        this.setupSocialButtons();
        this.setupGentleEffects();
    }

    bindEvents() {
        if (!this.form) return;

        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        if (this.emailInput) {
            this.emailInput.addEventListener('blur', () => this.validateEmail());
            this.emailInput.addEventListener('input', () => this.clearError('email'));
            this.emailInput.placeholder = " ";
        }

        if (this.passwordInput) {
            this.passwordInput.addEventListener('blur', () => this.validatePassword());
            this.passwordInput.addEventListener('input', () => this.clearError('password'));
            this.passwordInput.placeholder = " ";
        }

        if (this.usernameInput) {
            this.usernameInput.addEventListener('blur', () => this.validateUsername());
            this.usernameInput.addEventListener('input', () => this.clearError('username'));
            this.usernameInput.placeholder = " ";
        }

        if (this.passwordConfirm) {
            this.passwordConfirm.addEventListener('blur', () => this.validatePasswordConfirm());
            this.passwordConfirm.addEventListener('input', () => this.clearError('passwordConfirm'));
            this.passwordConfirm.placeholder = " ";
        }
    }

    setupPasswordToggle() {
        // FIX: guard null — bản gốc crash nếu passwordToggle hoặc passwordInput không tồn tại
        if (!this.passwordToggle || !this.passwordInput) return;

        this.passwordToggle.addEventListener('click', () => {
            const type = this.passwordInput.type === 'password' ? 'text' : 'password';
            this.passwordInput.type = type;
            this.passwordToggle.classList.toggle('toggle-active', type === 'text');
            this.triggerGentleRipple(this.passwordToggle);
        });
    }

    setupSocialButtons() {
        this.socialButtons.forEach(button => {
            button.addEventListener('click', () => {
                // FIX: chặn click khi đang loading
                if (this._socialLoading.get(button)) return;

                const provider = button.querySelector('span')?.textContent.trim(); // FIX: optional chaining tránh crash nếu không có <span>
                this.handleSocialLogin(provider, button);
            });
        });
    }

    setupGentleEffects() {
        // FIX: bản gốc crash nếu bất kỳ input nào là null (vd: form login không có username/passwordConfirm)
        [this.emailInput, this.passwordInput, this.usernameInput, this.passwordConfirm]
            .filter(Boolean)
            .forEach(input => {
                input.addEventListener('focus', (e) => {
                    this.triggerSoftFocus(e.target.closest('.field-container'));
                });
                input.addEventListener('blur', (e) => {
                    this.releaseSoftFocus(e.target.closest('.field-container'));
                });
            });

        this.addGentleClickEffects();
    }

    triggerSoftFocus(container) {
        if (!container) return; // FIX: guard null
        container.style.transition = 'all 0.3s ease';
        container.style.transform = 'translateY(-1px)';
    }

    releaseSoftFocus(container) {
        if (!container) return; // FIX: guard null
        container.style.transform = 'translateY(0)';
    }

    triggerGentleRipple(element) {
        element.style.transform = 'scale(0.95)';
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 150);
    }

    addGentleClickEffects() {
        const interactiveElements = document.querySelectorAll('.comfort-button, .social-soft, .gentle-checkbox');
        interactiveElements.forEach(element => {
            element.addEventListener('mousedown', () => { element.style.transform = 'scale(0.98)'; });
            element.addEventListener('mouseup', () => { element.style.transform = 'scale(1)'; });
            element.addEventListener('mouseleave', () => { element.style.transform = 'scale(1)'; });
        });
    }

    validateUsername(strict = false) {
        // FIX: guard null — bản gốc crash nếu usernameInput không có trong DOM
        if (!this.usernameInput) return true;

        const username = this.usernameInput.value.trim();
        if (!username) { this.showError('username', 'Please enter your username'); return false; }
        if (!strict) {
            this.clearError('username');
            return true;
        }

        const usernameRegex = /^[A-Za-z][A-Za-z0-9._]{4,31}$/;
        if (!usernameRegex.test(username)) {
            this.showError('username', 'Username must start with a letter and be 5-32 chars (a-z, 0-9, . _)');
            return false;
        }
        this.clearError('username');
        return true;
    }

    validateEmail() {
        // FIX: guard null
        if (!this.emailInput) return true;

        const email = this.emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email) { this.showError('email', 'Please enter your email address'); return false; }
        if (!emailRegex.test(email)) { this.showError('email', 'Please enter a valid email address'); return false; }
        this.clearError('email');
        return true;
    }

    validatePassword(strict = false) {
        // FIX: guard null
        if (!this.passwordInput) return true;

        const password = this.passwordInput.value;
        if (!password) { this.showError('password', 'Please enter your password'); return false; }
        if (!strict) {
            this.clearError('password');
            return true;
        }

        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])\S{8,64}$/;
        if (!passwordRegex.test(password)) {
            this.showError('password', 'Password must be 8-64 chars with upper, lower, number and symbol');
            return false;
        }
        this.clearError('password');
        return true;
    }

    validatePasswordConfirm() {
        // FIX: guard null
        if (!this.passwordConfirm || !this.passwordInput) return true;

        const password = this.passwordInput.value;
        const confirm = this.passwordConfirm.value;
        if (!confirm) { this.showError('passwordConfirm', 'Please confirm your password'); return false; }
        if (password !== confirm) { this.showError('passwordConfirm', 'Passwords do not match'); return false; }
        this.clearError('passwordConfirm');
        return true;
    }

    showError(field, message) {
        const input = document.getElementById(field);
        if (!input) return; // FIX: guard null

        const softField = input.closest('.soft-field');
        const errorElement = document.getElementById(`${field}Error`);
        if (!softField || !errorElement) return; // FIX: guard null

        // FIX: hủy timer clearError đang chờ để tránh xóa nhầm message mới
        if (this._clearErrorTimers[field]) {
            clearTimeout(this._clearErrorTimers[field]);
            delete this._clearErrorTimers[field];
        }

        softField.classList.add('error');
        errorElement.textContent = message;
        errorElement.classList.add('show');
        this.triggerGentleShake(softField);
    }

    clearError(field) {
        const input = document.getElementById(field);
        if (!input) return; // FIX: guard null

        const softField = input.closest('.soft-field');
        const errorElement = document.getElementById(`${field}Error`);
        if (!softField || !errorElement) return; // FIX: guard null

        softField.classList.remove('error');
        errorElement.classList.remove('show');

        // FIX: lưu timer để cancel nếu showError được gọi lại trong 300ms
        if (this._clearErrorTimers[field]) clearTimeout(this._clearErrorTimers[field]);
        this._clearErrorTimers[field] = setTimeout(() => {
            if (!errorElement.classList.contains('show')) errorElement.textContent = '';
            delete this._clearErrorTimers[field];
        }, 300);
    }

    triggerGentleShake(element) {
        element.style.animation = 'none';
        element.style.transform = 'translateX(2px)';
        setTimeout(() => { element.style.transform = 'translateX(-2px)'; }, 100);
        setTimeout(() => { element.style.transform = 'translateX(0)'; }, 200);
    }

    async handleSubmit(e) {
        const formAction = (this.form?.getAttribute('action') || '').toLowerCase();
        const isLoginForm = formAction.includes('login');
        const isRegisterForm = formAction.includes('register');

        // Login/Register pages: validate and let browser submit form to servlet.
        if (isLoginForm || isRegisterForm) {
            const isUsernameValid = this.validateUsername(isRegisterForm);
            const isPasswordValid = this.validatePassword(isRegisterForm);
            const isEmailValid = isRegisterForm ? this.validateEmail() : true;
            const isConfirmValid = isRegisterForm ? this.validatePasswordConfirm() : true;

            if (!isUsernameValid || !isPasswordValid || !isEmailValid || !isConfirmValid) {
                e.preventDefault();
                return;
            }

            if (this._isSubmitting) {
                e.preventDefault();
                return;
            }

            this._isSubmitting = true;
            this.setLoading(true);
            return;
        }

        e.preventDefault();

        // Non-login forms keep existing demo behavior.
        if (this._isSubmitting) return;

        const isUsernameValid = this.validateUsername();
        const isEmailValid = this.validateEmail();
        const isPasswordValid = this.validatePassword();
        const isConfirmValid = this.validatePasswordConfirm();

        if (!isUsernameValid || !isEmailValid || !isPasswordValid || !isConfirmValid) return;

        this._isSubmitting = true;
        this.setLoading(true);

        try {
            await new Promise(resolve => setTimeout(resolve, 2500));
            this.showGentleSuccess();
        } catch (error) {
            this.showError('password', 'Sign in failed. Please try again.');
        } finally {
            this._isSubmitting = false;
            this.setLoading(false);
        }
    }

    async handleSocialLogin(provider, button) {
        if (!button) return;

        // FIX: set guard trước async, dùng try/finally đảm bảo luôn restore
        this._socialLoading.set(button, true);

        const originalHTML = button.innerHTML;
        button.style.pointerEvents = 'none';
        button.style.opacity = '0.7';

        button.innerHTML = `
            <div class="social-background"></div>
            <div class="gentle-spinner">
                <div class="spinner-circle"></div>
            </div>
            <span>Connecting...</span>
            <div class="social-glow"></div>
        `;

        try {
            await new Promise(resolve => setTimeout(resolve, 2000));
        } catch (error) {
            console.error(`${provider} sign in error:`, error.message);
        } finally {
            // FIX: restore chắc chắn xảy ra, kiểm tra button còn trong DOM
            if (document.body.contains(button)) {
                button.style.pointerEvents = 'auto';
                button.style.opacity = '1';
                button.innerHTML = originalHTML;
            }
            this._socialLoading.set(button, false);
        }
    }

    setLoading(loading) {
        if (!this.submitButton) return; // FIX: guard null
        this.submitButton.classList.toggle('loading', loading);
        this.submitButton.disabled = loading;

        this.socialButtons.forEach(button => {
            button.style.pointerEvents = loading ? 'none' : 'auto';
            button.style.opacity = loading ? '0.5' : '1';
        });
    }

    showGentleSuccess() {
        if (!this.successMessage) return; // FIX: guard null

        this.form.style.transform = 'scale(0.95)';
        this.form.style.opacity = '0';
        this.form.style.filter = 'blur(1px)';

        setTimeout(() => {
            this.form.style.display = 'none';

            // FIX: guard null trước khi ẩn từng element
            const comfortSocial = document.querySelector('.comfort-social');
            const comfortSignup = document.querySelector('.comfort-signup');
            const gentleDivider = document.querySelector('.gentle-divider');
            const accept = document.getElementById('accept');
            if (accept) accept.style.display = 'none';
            if (comfortSocial) comfortSocial.style.display = 'none';
            if (comfortSignup) comfortSignup.style.display = 'none';
            if (gentleDivider) gentleDivider.style.display = 'none';

            this.successMessage.classList.add('show');
            this.triggerSuccessGlow();
        }, 300);

        setTimeout(() => {
            console.log('Welcome! Taking you to your dashboard...');
            // window.location.href = '/dashboard';
        }, 3500);
    }

    triggerSuccessGlow() {
        const card = document.querySelector('.soft-card');
        if (!card) return; // FIX: guard null

        card.style.boxShadow = `
            0 20px 40px rgba(240, 206, 170, 0.2),
            0 8px 24px rgba(240, 206, 170, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.8)
        `;

        setTimeout(() => {
            card.style.boxShadow = `
                0 20px 40px rgba(0, 0, 0, 0.03),
                0 8px 24px rgba(0, 0, 0, 0.02),
                inset 0 1px 0 rgba(255, 255, 255, 0.8)
            `;
        }, 2000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SoftMinimalismLoginForm();
});