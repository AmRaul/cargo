import { motion } from 'framer-motion'

interface HeroProps {
  onOrderClick: () => void
}

export default function Hero({ onOrderClick }: HeroProps) {
  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 text-white">
      {/* Фоновые элементы */}
      <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
      <div className="absolute top-0 right-0 w-96 h-96 bg-accent-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-primary-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              Грузоперевозки из ОАЭ и Турции в РФ
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              Надежная доставка под ключ с полным сопровождением на всех этапах
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <button
                onClick={onOrderClick}
                className="bg-accent-500 hover:bg-accent-600 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                Оставить заявку
              </button>
              <a
                href="#features"
                className="bg-white/10 hover:bg-white/20 backdrop-blur-sm text-white px-8 py-4 rounded-lg text-lg font-semibold transition-all border border-white/30"
              >
                Узнать больше
              </a>
            </div>

            <div className="mt-12 grid grid-cols-3 gap-6">
              <div>
                <div className="text-3xl font-bold text-accent-300">5+</div>
                <div className="text-sm text-primary-200">лет опыта</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent-300">350+</div>
                <div className="text-sm text-primary-200">доставок</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-accent-300">24/7</div>
                <div className="text-sm text-primary-200">поддержка</div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="hidden md:block"
          >
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-accent-400 to-accent-600 rounded-2xl transform rotate-3"></div>
              <div className="relative bg-white rounded-2xl p-8 shadow-2xl transform -rotate-1">
                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                      <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <div className="flex-1">
                      <div className="text-sm text-gray-500">Статус груза</div>
                      <div className="font-semibold text-gray-900">В пути → Москва</div>
                    </div>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div className="h-full w-3/4 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full"></div>
                  </div>
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="bg-primary-50 rounded-lg p-3">
                      <div className="text-xs text-gray-500">Откуда</div>
                      <div className="font-semibold text-gray-900">Дубай 🇦🇪</div>
                    </div>
                    <div className="bg-primary-50 rounded-lg p-3">
                      <div className="text-xs text-gray-500">Куда</div>
                      <div className="font-semibold text-gray-900">Москва 🇷🇺</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
