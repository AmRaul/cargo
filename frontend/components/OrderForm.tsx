import { useState } from 'react'
import { useForm } from 'react-hook-form'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'

interface OrderFormProps {
  isOpen: boolean
  onClose: () => void
}

interface FormData {
  client_name: string
  client_phone: string
  client_email?: string
  company_name?: string
  route: 'uae_to_rf' | 'turkey_to_rf'
  cargo_type: string
  cargo_weight?: number
  cargo_volume?: number
  description?: string
  pickup_address?: string
  delivery_address?: string
}

export default function OrderForm({ isOpen, onClose }: OrderFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<FormData>()

  const onSubmit = async (data: FormData) => {
    setIsSubmitting(true)
    setSubmitError(null)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      await axios.post(`${apiUrl}/api/v1/orders/`, data)

      setSubmitSuccess(true)
      reset()

      setTimeout(() => {
        setSubmitSuccess(false)
        onClose()
      }, 3000)
    } catch (error) {
      console.error('Error submitting form:', error)
      setSubmitError('Произошла ошибка при отправке заявки. Пожалуйста, попробуйте еще раз.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed inset-0 z-50 overflow-y-auto"
          >
            <div className="min-h-screen px-4 flex items-center justify-center">
              <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-8">
                {/* Header */}
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-3xl font-bold text-gray-900">
                    Заявка на грузоперевозку
                  </h2>
                  <button
                    onClick={onClose}
                    className="text-gray-400 hover:text-gray-600 transition-colors"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                {submitSuccess ? (
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="text-center py-12"
                  >
                    <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">Заявка отправлена!</h3>
                    <p className="text-gray-600">Наш менеджер свяжется с вами в ближайшее время</p>
                  </motion.div>
                ) : (
                  <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                    {/* Контактная информация */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Контактная информация</h3>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Имя <span className="text-red-500">*</span>
                          </label>
                          <input
                            {...register('client_name', { required: 'Обязательное поле' })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                            placeholder="Иван Иванов"
                          />
                          {errors.client_name && (
                            <p className="text-red-500 text-sm mt-1">{errors.client_name.message}</p>
                          )}
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Телефон <span className="text-red-500">*</span>
                          </label>
                          <input
                            {...register('client_phone', {
                              required: 'Обязательное поле',
                              pattern: {
                                value: /^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$/,
                                message: 'Неверный формат телефона'
                              }
                            })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                            placeholder="+7 (999) 123-45-67"
                          />
                          {errors.client_phone && (
                            <p className="text-red-500 text-sm mt-1">{errors.client_phone.message}</p>
                          )}
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Email
                          </label>
                          <input
                            {...register('client_email', {
                              pattern: {
                                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                                message: 'Неверный формат email'
                              }
                            })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                            placeholder="email@example.com"
                          />
                          {errors.client_email && (
                            <p className="text-red-500 text-sm mt-1">{errors.client_email.message}</p>
                          )}
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Компания
                          </label>
                          <input
                            {...register('company_name')}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                            placeholder="ООО Компания"
                          />
                        </div>
                      </div>
                    </div>

                    {/* Детали груза */}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Детали груза</h3>
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Направление <span className="text-red-500">*</span>
                          </label>
                          <select
                            {...register('route', { required: 'Обязательное поле' })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                          >
                            <option value="">Выберите направление</option>
                            <option value="uae_to_rf">🇦🇪 ОАЭ → Россия</option>
                            <option value="turkey_to_rf">🇹🇷 Турция → Россия</option>
                          </select>
                          {errors.route && (
                            <p className="text-red-500 text-sm mt-1">{errors.route.message}</p>
                          )}
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Тип груза <span className="text-red-500">*</span>
                          </label>
                          <input
                            {...register('cargo_type', { required: 'Обязательное поле' })}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                            placeholder="Например: электроника, одежда, мебель"
                          />
                          {errors.cargo_type && (
                            <p className="text-red-500 text-sm mt-1">{errors.cargo_type.message}</p>
                          )}
                        </div>

                        <div className="grid md:grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Вес (кг)
                            </label>
                            <input
                              type="number"
                              step="0.01"
                              {...register('cargo_weight', { min: { value: 0, message: 'Должно быть больше 0' } })}
                              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                              placeholder="100"
                            />
                            {errors.cargo_weight && (
                              <p className="text-red-500 text-sm mt-1">{errors.cargo_weight.message}</p>
                            )}
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Объем (м³)
                            </label>
                            <input
                              type="number"
                              step="0.01"
                              {...register('cargo_volume', { min: { value: 0, message: 'Должно быть больше 0' } })}
                              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                              placeholder="1.5"
                            />
                            {errors.cargo_volume && (
                              <p className="text-red-500 text-sm mt-1">{errors.cargo_volume.message}</p>
                            )}
                          </div>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Описание груза
                          </label>
                          <textarea
                            {...register('description')}
                            rows={3}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                            placeholder="Дополнительная информация о грузе"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Адрес забора груза
                          </label>
                          <input
                            {...register('pickup_address')}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                            placeholder="Город, улица, дом"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Адрес доставки
                          </label>
                          <input
                            {...register('delivery_address')}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                            placeholder="Город, улица, дом"
                          />
                        </div>
                      </div>
                    </div>

                    {submitError && (
                      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                        {submitError}
                      </div>
                    )}

                    {/* Buttons */}
                    <div className="flex gap-4">
                      <button
                        type="button"
                        onClick={onClose}
                        className="flex-1 px-6 py-3 border border-gray-300 rounded-lg text-gray-700 font-semibold hover:bg-gray-50 transition-colors"
                      >
                        Отмена
                      </button>
                      <button
                        type="submit"
                        disabled={isSubmitting}
                        className="flex-1 px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-lg font-semibold hover:from-primary-700 hover:to-primary-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isSubmitting ? 'Отправка...' : 'Отправить заявку'}
                      </button>
                    </div>
                  </form>
                )}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
