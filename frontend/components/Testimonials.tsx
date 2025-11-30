import { motion } from 'framer-motion'
import { useState } from 'react'

const testimonials = [
  {
    name: 'Алексей Петров',
    company: 'ООО "ТехноИмпорт"',
    role: 'Директор по закупкам',
    avatar: '👨‍💼',
    rating: 5,
    text: 'Работаем с Cargo Express уже 3 года. Всегда четкие сроки, прозрачное ценообразование и отличная поддержка. Доставили сложный груз из Дубая за 5 дней - это рекорд!',
    route: 'ОАЭ → Москва'
  },
  {
    name: 'Марина Соколова',
    company: 'Интернет-магазин "Восток"',
    role: 'Владелец',
    avatar: '👩‍💼',
    rating: 5,
    text: 'Отличный сервис! Помогли с таможенным оформлением, взяли на себя все хлопоты. Груз пришел в целости и сохранности. Рекомендую всем!',
    route: 'Турция → Санкт-Петербург'
  },
  {
    name: 'Дмитрий Иванов',
    company: 'ИП Иванов',
    role: 'Предприниматель',
    avatar: '👨‍💻',
    rating: 5,
    text: 'Первый раз заказывал доставку из Стамбула. Менеджер все подробно объяснил, помог с документами. Груз пришел даже раньше срока. Цены адекватные.',
    route: 'Турция → Екатеринбург'
  },
  {
    name: 'Елена Смирнова',
    company: 'Торговый дом "Азия"',
    role: 'Менеджер по логистике',
    avatar: '👩',
    rating: 5,
    text: 'Профессиональный подход на всех этапах. Особенно понравилась возможность отслеживания груза онлайн. Всегда в курсе где находится товар.',
    route: 'ОАЭ → Новосибирск'
  }
]

export default function Testimonials() {
  const [activeIndex, setActiveIndex] = useState(0)

  return (
    <section className="py-20 bg-gradient-to-br from-slate-50 to-slate-100 relative overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-0 left-0 w-64 h-64 bg-primary-200 rounded-full opacity-20 -translate-x-1/2 -translate-y-1/2"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-accent-200 rounded-full opacity-20 translate-x-1/2 translate-y-1/2"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Отзывы наших клиентов
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Более 100 компаний доверяют нам доставку своих грузов
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -5 }}
              className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer"
              onClick={() => setActiveIndex(index)}
            >
              {/* Rating stars */}
              <div className="flex gap-1 mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <span key={i} className="text-yellow-400 text-xl">⭐</span>
                ))}
              </div>

              {/* Quote */}
              <p className="text-gray-700 leading-relaxed mb-6 italic">
                "{testimonial.text}"
              </p>

              {/* Route badge */}
              <div className="inline-block bg-primary-100 text-primary-700 px-4 py-1 rounded-full text-sm font-semibold mb-6">
                📍 {testimonial.route}
              </div>

              {/* Author info */}
              <div className="flex items-center gap-4 border-t pt-4">
                <div className="text-5xl">{testimonial.avatar}</div>
                <div>
                  <div className="font-bold text-gray-900">{testimonial.name}</div>
                  <div className="text-sm text-gray-600">{testimonial.role}</div>
                  <div className="text-sm text-primary-600 font-semibold">{testimonial.company}</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Trust indicators */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="bg-white rounded-2xl p-8 shadow-lg"
        >
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl mb-2">🏆</div>
              <div className="text-3xl font-bold text-primary-600 mb-1">4.9/5</div>
              <div className="text-gray-600">Средний рейтинг</div>
            </div>
            <div>
              <div className="text-4xl mb-2">💼</div>
              <div className="text-3xl font-bold text-primary-600 mb-1">150+</div>
              <div className="text-gray-600">Компаний-партнеров</div>
            </div>
            <div>
              <div className="text-4xl mb-2">📝</div>
              <div className="text-3xl font-bold text-primary-600 mb-1">200+</div>
              <div className="text-gray-600">Положительных отзывов</div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
