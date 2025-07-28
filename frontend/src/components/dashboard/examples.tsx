'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import {
  BarChart3,
  Bot,
  Briefcase,
  Settings,
  Target,
  PenTool,
  DollarSign,
  Users,
  TrendingUp,
  Code,
  Shield,
  Brain,
  Globe,
  Heart,
  Calendar,
  Zap,
  Rocket,
  Camera,
  Sparkles,
  Home,
  MapPin,
  Star,
  Clock,
  Key,
  Search,
  FileText,
  CreditCard,
  CheckCircle,
  Building,
  RefreshCw
} from 'lucide-react'

export interface PromptExample {
  title: string
  query: string
  icon: React.ReactNode
}

const allPrompts: PromptExample[] = [
  {
    title: 'Find vacation rental in Miami',
    query: 'Help me find a beachfront vacation rental in Miami for 4 guests, 3 nights in March. Include amenities like pool, WiFi, and parking. Show availability and pricing.',
    icon: <Home className="text-blue-700 dark:text-blue-400" size={16} />,
  },
  {
    title: 'Apartment hunting in NYC',
    query: 'I need a 2-bedroom apartment in Manhattan under $4000/month. Long-term lease preferred. Must be pet-friendly and near subway. Help me find and schedule viewings.',
    icon: <Building className="text-green-700 dark:text-green-400" size={16} />,
  },
  {
    title: 'List my property for rent',
    query: 'Help me create a professional listing for my 3-bedroom house. Generate description, set competitive pricing, and suggest the best rental platforms to use.',
    icon: <PenTool className="text-rose-700 dark:text-rose-400" size={16} />,
  },
  {
    title: 'Short-term rental investment',
    query: 'Analyze potential ROI for buying a property in Austin for Airbnb. Include market research, estimated occupancy rates, and monthly revenue projections.',
    icon: <TrendingUp className="text-purple-700 dark:text-purple-400" size={16} />,
  },
  {
    title: 'Rental application assistant',
    query: 'Help me prepare a strong rental application for a downtown loft. Include required documents, references, and tips to stand out to landlords.',
    icon: <FileText className="text-orange-700 dark:text-orange-400" size={16} />,
  },
  {
    title: 'Property viewing scheduler',
    query: 'Coordinate viewing appointments for 5 apartments this weekend. Send confirmation emails to landlords and create an optimized viewing route.',
    icon: <Calendar className="text-indigo-700 dark:text-indigo-400" size={16} />,
  },
  {
    title: 'Rental market analysis',
    query: 'Create a comprehensive rental market report for Seattle. Include average prices by neighborhood, trends, and best areas for different budgets.',
    icon: <BarChart3 className="text-emerald-700 dark:text-emerald-400" size={16} />,
  },
  {
    title: 'Lease negotiation help',
    query: 'Help me negotiate better terms for a 1-year lease. Suggest reasonable requests for rent reduction, pet policy, and lease flexibility.',
    icon: <DollarSign className="text-cyan-700 dark:text-cyan-400" size={16} />,
  },
  {
    title: 'Property damage assessment',
    query: 'Document and assess rental property damage after tenant move-out. Create detailed report with photos and estimated repair costs for security deposit deduction.',
    icon: <Shield className="text-teal-700 dark:text-teal-400" size={16} />,
  },
  {
    title: 'Airbnb listing optimization',
    query: 'Optimize my Airbnb listing to increase bookings. Improve photos, description, pricing strategy, and guest communication templates.',
    icon: <Star className="text-violet-700 dark:text-violet-400" size={16} />,
  },
  {
    title: 'Tenant screening process',
    query: 'Create a comprehensive tenant screening checklist including credit checks, references, employment verification, and legal compliance requirements.',
    icon: <Users className="text-red-700 dark:text-red-400" size={16} />,
  },
  {
    title: 'Corporate housing search',
    query: 'Find short-term corporate housing in Chicago for 30 days. Fully furnished, near financial district, with business amenities and flexible check-in.',
    icon: <Briefcase className="text-pink-700 dark:text-pink-400" size={16} />,
  },
  {
    title: 'Rental property maintenance',
    query: 'Schedule quarterly maintenance for my rental properties. Coordinate HVAC service, pest control, and safety inspections. Track costs and create reports.',
    icon: <Settings className="text-blue-600 dark:text-blue-300" size={16} />,
  },
  {
    title: 'Guest check-in automation',
    query: 'Create an automated check-in system for my vacation rental. Include keyless entry instructions, house rules, and emergency contacts for guests.',
    icon: <Key className="text-red-600 dark:text-red-300" size={16} />,
  },
  {
    title: 'Rental income tracking',
    query: 'Set up a system to track rental income, expenses, and tax deductions. Include rent collection, maintenance costs, and quarterly reports.',
    icon: <Target className="text-amber-700 dark:text-amber-400" size={16} />,
  },
  {
    title: 'Property photo shoot',
    query: 'Plan a professional photo shoot for my rental listing. Schedule photographer, stage the property, and create a shot list highlighting key features.',
    icon: <Camera className="text-yellow-600 dark:text-yellow-300" size={16} />,
  },
  {
    title: 'Neighborhood guide creation',
    query: 'Create a comprehensive neighborhood guide for my rental guests. Include restaurants, attractions, transportation, and local recommendations.',
    icon: <MapPin className="text-orange-600 dark:text-orange-300" size={16} />,
  },
  {
    title: 'Rental price analysis',
    query: 'Analyze current market rates for similar properties in my area. Suggest optimal pricing strategy for maximum occupancy and revenue.',
    icon: <Zap className="text-slate-700 dark:text-slate-400" size={16} />,
  },
  {
    title: 'Student housing search',
    query: 'Help college student find affordable housing near campus. Include roommate matching, lease terms, and proximity to university facilities.',
    icon: <Brain className="text-stone-700 dark:text-stone-400" size={16} />,
  },
  {
    title: 'Property investment calculator',
    query: 'Calculate potential returns on a rental property investment. Include purchase price, renovation costs, monthly expenses, and break-even analysis.',
    icon: <Bot className="text-fuchsia-700 dark:text-fuchsia-400" size={16} />,
  },
];

// Function to get random prompts
const getRandomPrompts = (count: number = 3): PromptExample[] => {
  const shuffled = [...allPrompts].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
};

export const Examples = ({
  onSelectPrompt,
}: {
  onSelectPrompt?: (query: string) => void;
}) => {
  const [displayedPrompts, setDisplayedPrompts] = useState<PromptExample[]>([]);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Initialize with random prompts on mount
  useEffect(() => {
    setDisplayedPrompts(getRandomPrompts(3));
  }, []);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setDisplayedPrompts(getRandomPrompts(3));
    setTimeout(() => setIsRefreshing(false), 300);
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4">
      <div className="group relative">
        <div className="flex gap-2 justify-center py-2">
          {displayedPrompts.map((prompt, index) => (
            <motion.div
              key={`${prompt.title}-${index}`}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{
                duration: 0.3,
                delay: index * 0.03,
                ease: "easeOut"
              }}
            >
              <Button
                variant="outline"
                className="w-fit h-fit px-3 py-2 rounded-full border-neutral-200 dark:border-neutral-800 bg-neutral-50 hover:bg-neutral-100 dark:bg-neutral-900 dark:hover:bg-neutral-800 text-sm font-normal text-muted-foreground hover:text-foreground transition-colors"
                onClick={() => onSelectPrompt && onSelectPrompt(prompt.query)}
              >
                <div className="flex items-center gap-2">
                  <div className="flex-shrink-0">
                    {React.cloneElement(prompt.icon as React.ReactElement, { size: 14 })}
                  </div>
                  <span className="whitespace-nowrap">{prompt.title}</span>
                </div>
              </Button>
            </motion.div>
          ))}
        </div>

        {/* Refresh button that appears on hover */}
        <Button
          variant="ghost"
          size="sm"
          onClick={handleRefresh}
          className="absolute -top-4 right-1 h-5 w-5 p-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:bg-neutral-100 dark:hover:bg-neutral-800"
        >
          <motion.div
            animate={{ rotate: isRefreshing ? 360 : 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
          >
            <RefreshCw size={10} className="text-muted-foreground" />
          </motion.div>
        </Button>
      </div>
    </div>
  );
};