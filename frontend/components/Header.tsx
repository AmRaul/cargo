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
