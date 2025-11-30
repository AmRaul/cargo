import { motion } from 'framer-motion'
import { useState } from 'react'

const shippingTypes = [
  {
    id: 'air',
    title: 'Авиа доставка',
    icon: '✈️',
    time: '3-7 дней',
    price: 'от $15/кг',
    features: [
      'Самый быстрый способ',
      'Подходит для срочных грузов',
      'Доставка в любую точку мира',
      'Страховка груза',
      'Отслеживание в реальном времени'
    ],
    color: 'from-sky-400 to-blue-600',
    bgImage: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    id: 'sea',
    title: 'Морская доставка',
    icon: '🚢',
    time: '25-45 дней',
    price: 'от $2/кг',
    features: [
      'Экономичный вариант',
      'Большие объемы грузов',
      'Контейнерные перевозки',
      'FCL и LCL варианты',
      'Оптимально для негабарита'
    ],
    color: 'from-cyan-400 to-teal-600',
    bgImage: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    id: 'ground',
    title: 'Авто доставка',
    icon: '🚚',
    time: '7-14 дней',
    price: 'от $5/кг',
    features: [
      'Оптимальная скорость',
      'Доставка до двери',
      'Подходит для Турции',
      'Гибкие маршруты',
      'Доступные цены'
    ],
    color: 'from-orange-400 to-red-600',
    bgImage: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  }
]

export default function ShippingTypes() {
  const [activeType, setActiveType] = useState('air')

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Типы доставки
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Выберите оптимальный способ доставки для вашего груза
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {shippingTypes.map((type, index) => (
            <motion.div
              key={type.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.15 }}
              onHoverStart={() => setActiveType(type.id)}
              className={`relative rounded-3xl p-8 cursor-pointer transition-all duration-300 ${
                activeType === type.id
                  ? 'transform scale-105 shadow-2xl'
                  : 'shadow-lg hover:shadow-xl'
              }`}
              style={{
                background: activeType === type.id ? type.bgImage : '#ffffff',
                border: activeType === type.id ? 'none' : '2px solid #e5e7eb'
              }}
            >
              {/* Icon */}
              <div className="text-7xl mb-4 text-center transform transition-transform duration-300 hover:scale-110">
                {type.icon}
              </div>

              {/* Title */}
              <h3
                className={`text-2xl font-bold mb-2 text-center transition-colors ${
                  activeType === type.id ? 'text-white' : 'text-gray-900'
                }`}
              >
                {type.title}
              </h3>

              {/* Time & Price */}
              <div className="flex justify-between items-center mb-6">
                <div
                  className={`text-sm font-semibold ${
                    activeType === type.id ? 'text-white/90' : 'text-gray-600'
                  }`}
                >
                  ⏱️ {type.time}
                </div>
                <div
                  className={`text-lg font-bold ${
                    activeType === type.id ? 'text-white' : 'text-primary-600'
                  }`}
                >
                  {type.price}
                </div>
              </div>

              {/* Features */}
              <ul className="space-y-3">
                {type.features.map((feature, idx) => (
                  <li
                    key={idx}
                    className={`flex items-start text-sm ${
                      activeType === type.id ? 'text-white/90' : 'text-gray-600'
                    }`}
                  >
                    <span className="mr-2">✓</span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              {/* CTA Button */}
              <button
                className={`mt-6 w-full py-3 rounded-xl font-semibold transition-all ${
                  activeType === type.id
                    ? 'bg-white text-primary-600 hover:bg-gray-100'
                    : 'bg-primary-600 text-white hover:bg-primary-700'
                }`}
              >
                Узнать подробнее
              </button>
            </motion.div>
          ))}
        </div>

        {/* Additional info */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.5 }}
          className="mt-12 text-center"
        >
          <p className="text-gray-600 mb-4">
            💡 Не уверены какой тип доставки выбрать? Наши менеджеры помогут!
          </p>
          <button className="bg-gradient-to-r from-primary-600 to-primary-700 text-white px-8 py-3 rounded-lg font-semibold hover:from-primary-700 hover:to-primary-800 transition-all shadow-lg">
            Получить консультацию
          </button>
        </motion.div>
      </div>
    </section>
  )
}
