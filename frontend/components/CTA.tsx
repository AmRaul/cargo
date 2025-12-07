import { motion } from 'framer-motion'

interface CTAProps {
  onOrderClick: () => void
}

export default function CTA({ onOrderClick }: CTAProps) {
  return (
    <section className="py-20 relative overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900"></div>

      {/* Animated shapes */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-accent-400 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-pink-400 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center"
        >
          <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Готовы отправить груз?
          </h2>
          <p className="text-xl md:text-2xl text-primary-100 mb-12 max-w-3xl mx-auto">
            Получите бесплатный расчет стоимости. Никаких скрытых платежей.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <motion.button
              onClick={onOrderClick}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-accent-500 hover:bg-accent-600 text-white px-10 py-5 rounded-xl text-lg font-bold shadow-2xl transition-all inline-flex items-center gap-3"
            >
              <span>📦</span>
              Рассчитать стоимость
            </motion.button>
          </div>

          {/* Benefits */}
          <div className="grid md:grid-cols-4 gap-6 mt-16">
            {[
              { icon: '🚀', text: 'Быстрая обработка заявок' },
              { icon: '💰', text: 'Лучшие цены на рынке' },
              { icon: '🛡️', text: 'Гарантия безопасности' },
              { icon: '🎁', text: 'Скидки постоянным клиентам' }
            ].map((benefit, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20"
              >
                <div className="text-4xl mb-3">{benefit.icon}</div>
                <div className="text-white font-semibold">{benefit.text}</div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
