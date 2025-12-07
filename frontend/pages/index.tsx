import Head from 'next/head'
import { useState } from 'react'
import Header from '@/components/Header'
import Hero from '@/components/Hero'
import Stats from '@/components/Stats'
import Features from '@/components/Features'
import HowItWorks from '@/components/HowItWorks'
import ShippingTypes from '@/components/ShippingTypes'
import CTA from '@/components/CTA'
import FAQ from '@/components/FAQ'
import OrderForm from '@/components/OrderForm'
import Footer from '@/components/Footer'

export default function Home() {
  const [showForm, setShowForm] = useState(false)

  return (
    <>
      <Head>
        <title>CargoHub - Грузоперевозки из ОАЭ и Турции в РФ</title>
        <meta name="description" content="Надежные грузоперевозки из ОАЭ и Турции в Россию. Доставка под ключ с полным сопровождением." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
        <link rel="icon" type="image/svg+xml" sizes="32x32" href="/favicon-32x32.svg" />
        <link rel="apple-touch-icon" href="/logo-v1-updated.svg" />
      </Head>

      <Header onOrderClick={() => setShowForm(true)} />

      <main className="min-h-screen pt-20">
        <Hero onOrderClick={() => setShowForm(true)} />
        <Stats />
        <Features />
        <HowItWorks />
        <ShippingTypes />
        <CTA onOrderClick={() => setShowForm(true)} />
        <FAQ />
        <OrderForm isOpen={showForm} onClose={() => setShowForm(false)} />
        <Footer />
      </main>
    </>
  )
}
