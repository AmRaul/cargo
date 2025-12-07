import { motion } from 'framer-motion'

const steps = [
  {
    number: '01',
    title: 'Оставьте заявку',
    description: 'Заполните форму или свяжитесь с нами любым удобным способом',
    icon: '📝',
    color: 'from-blue-500 to-blue-600'
  },
  {
    number: '02',
    title: 'Расчет стоимости',
    description: 'Получите точный расчет стоимости доставки',
    icon: '💰',
    color: 'from-purple-500 to-purple-600'
  },
  {
    number: '03',
    title: 'Оформление документов',
    description: 'Берем на себя всю работу с таможней и документацией',
    icon: '📋',
    color: 'from-pink-500 to-pink-600'
  },
  {
    number: '04',
    title: 'Отправка груза',
    description: 'Забираем груз из точки отправления и начинаем доставку',
    icon: '🚚',
    color: 'from-orange-500 to-orange-600'
  },
  {
    number: '05',
    title: 'Получение груза',
    description: 'Доставляем груз по указанному адресу точно в срок',
    icon: '✅',
    color: 'from-teal-500 to-teal-600'
  }
]

export default function HowItWorks() {
  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Как мы работаем
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Простой и прозрачный процесс доставки вашего груза
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="relative group"
            >
              {/* Connecting line (hidden on mobile, shown on larger screens) */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-16 left-full w-full h-0.5 bg-gradient-to-r from-gray-300 to-transparent -z-10"></div>
              )}

              <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                {/* Number badge */}
                <div className={`inline-block bg-gradient-to-r ${step.color} text-white text-sm font-bold px-4 py-1 rounded-full mb-4`}>
                  {step.number}
                </div>

                {/* Icon */}
                <div className="text-6xl mb-4">{step.icon}</div>

                {/* Title */}
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                  {step.title}
                </h3>

                {/* Description */}
                <p className="text-gray-600 leading-relaxed">
                  {step.description}
                </p>

                {/* Hover indicator */}
                <div className="absolute bottom-0 left-0 w-0 h-1 bg-gradient-to-r from-primary-500 to-accent-500 group-hover:w-full transition-all duration-300 rounded-b-2xl"></div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
