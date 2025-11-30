import { motion } from 'framer-motion'

const stats = [
  { number: '350+', label: 'Успешных доставок', icon: '📦' },
  { number: '95%', label: 'Довольных клиентов', icon: '😊' },
  { number: '5+', label: 'Лет на рынке', icon: '🏆' },
  { number: '24/7', label: 'Поддержка клиентов', icon: '🎧' }
]

export default function Stats() {
  return (
    <section className="py-16 bg-gradient-to-r from-primary-600 to-primary-800 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute w-96 h-96 bg-white rounded-full -top-48 -left-48 animate-pulse"></div>
        <div className="absolute w-96 h-96 bg-white rounded-full -bottom-48 -right-48 animate-pulse delay-700"></div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="text-center"
            >
              <div className="text-4xl mb-2">{stat.icon}</div>
              <div className="text-4xl md:text-5xl font-bold text-white mb-2">
                {stat.number}
              </div>
              <div className="text-primary-100 text-sm md:text-base">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
