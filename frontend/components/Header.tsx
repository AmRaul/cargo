import { motion } from 'framer-motion'
import Image from 'next/image'

interface HeaderProps {
  onOrderClick: () => void
}

export default function Header({ onOrderClick }: HeaderProps) {
  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md shadow-md"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex items-center">
            <Image
              src="/logo-v2-updated.svg"
              alt="CargoHub"
              width={220}
              height={70}
              className="object-contain"
            />
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-gray-700 hover:text-primary-600 transition-colors font-medium">
              Преимущества
            </a>
            <a href="#how-it-works" className="text-gray-700 hover:text-primary-600 transition-colors font-medium">
              Как это работает
            </a>
            <a href="#faq" className="text-gray-700 hover:text-primary-600 transition-colors font-medium">
              FAQ
            </a>
          </nav>

          {/* CTA Button */}
          <div className="flex items-center gap-4">
            <a
              href="tel:+79991234567"
              className="hidden sm:flex items-center gap-2 text-gray-700 hover:text-primary-600 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <span className="font-semibold">+7 (999) 123-45-67</span>
            </a>
            <button
              onClick={onOrderClick}
              className="bg-gradient-to-r from-accent-500 to-accent-600 hover:from-accent-600 hover:to-accent-700 text-white px-6 py-2.5 rounded-lg font-semibold transition-all transform hover:scale-105 shadow-md hover:shadow-lg"
            >
              Заявка
            </button>
          </div>
        </div>
      </div>
    </motion.header>
  )
}
