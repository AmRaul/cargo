import Image from 'next/image'

export default function Footer() {
  return (
    <footer className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white py-16 relative overflow-hidden">
      {/* Decorative gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-900/20 to-transparent"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid md:grid-cols-4 gap-8 mb-12">
          {/* О компании */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <Image
                src="/logo-v3-updated.svg"
                alt="CargoHub"
                width={60}
                height={60}
                className="object-contain"
              />
              <h3 className="text-2xl font-bold text-accent-400">CargoHub</h3>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed mb-4">
              Профессиональные грузоперевозки из ОАЭ и Турции в Россию с полным сопровождением на всех этапах
            </p>
            {/* Social links */}
            <div className="flex gap-3">
              <a href="#" className="w-10 h-10 bg-gray-800 hover:bg-primary-600 rounded-full flex items-center justify-center transition-colors">
                <span className="text-xl">📱</span>
              </a>
              <a href="#" className="w-10 h-10 bg-gray-800 hover:bg-primary-600 rounded-full flex items-center justify-center transition-colors">
                <span className="text-xl">✉️</span>
              </a>
              <a href="#" className="w-10 h-10 bg-gray-800 hover:bg-primary-600 rounded-full flex items-center justify-center transition-colors">
                <span className="text-xl">💬</span>
              </a>
            </div>
          </div>

          {/* Контакты */}
          <div>
            <h4 className="font-bold text-lg mb-4 text-white">Контакты</h4>
            <ul className="space-y-3 text-sm text-gray-400">
              <li className="flex items-center gap-2 hover:text-white transition-colors cursor-pointer">
                <svg className="w-5 h-5 text-accent-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <span>+7 (999) 123-45-67</span>
              </li>
              <li className="flex items-center gap-2 hover:text-white transition-colors cursor-pointer">
                <svg className="w-5 h-5 text-accent-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>info@cargo-express.com</span>
              </li>
              <li className="flex items-center gap-2 text-accent-400">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="font-semibold">Работаем 24/7</span>
              </li>
            </ul>
          </div>

          {/* Услуги */}
          <div>
            <h4 className="font-bold text-lg mb-4 text-white">Услуги</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li className="hover:text-accent-400 transition-colors cursor-pointer">✈️ Авиа перевозки</li>
              <li className="hover:text-accent-400 transition-colors cursor-pointer">🚢 Морские перевозки</li>
              <li className="hover:text-accent-400 transition-colors cursor-pointer">🚚 Авто доставка</li>
              <li className="hover:text-accent-400 transition-colors cursor-pointer">📋 Таможенное оформление</li>
              <li className="hover:text-accent-400 transition-colors cursor-pointer">🛡️ Страхование грузов</li>
            </ul>
          </div>

          {/* Направления */}
          <div>
            <h4 className="font-bold text-lg mb-4 text-white">Направления</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li className="hover:text-accent-400 transition-colors cursor-pointer">🇦🇪 ОАЭ → Россия</li>
              <li className="hover:text-accent-400 transition-colors cursor-pointer">🇹🇷 Турция → Россия</li>
              <li className="opacity-60">🇨🇳 Китай → Россия (скоро)</li>
              <li className="opacity-60">🇪🇺 Европа → Россия (скоро)</li>
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-800 mb-8"></div>

        {/* Bottom section */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-gray-400">
          <p>&copy; {new Date().getFullYear()} CargoHub. Все права защищены.</p>
          <div className="flex gap-6">
            <a href="#" className="hover:text-accent-400 transition-colors">Политика конфиденциальности</a>
            <a href="#" className="hover:text-accent-400 transition-colors">Условия использования</a>
          </div>
        </div>

        {/* Trust badges */}
        <div className="mt-8 pt-8 border-t border-gray-800">
          <div className="flex flex-wrap justify-center items-center gap-8 opacity-60">
            <div className="text-center">
              <div className="text-2xl mb-1">🏆</div>
              <div className="text-xs">ISO 9001</div>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-1">✅</div>
              <div className="text-xs">Лицензия ФТС</div>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-1">🔒</div>
              <div className="text-xs">Secure SSL</div>
            </div>
            <div className="text-center">
              <div className="text-2xl mb-1">💼</div>
              <div className="text-xs">РТА член</div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
