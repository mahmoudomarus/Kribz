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
    title: 'Find Dubai Marina apartment',
    query: 'Help me find a 2-bedroom apartment in Dubai Marina under 8000 AED per month. Must have sea view, gym access, and be pet-friendly. Include nearby amenities and transportation options.',
    icon: <Home className="text-blue-700 dark:text-blue-400" size={16} />,
  },
  {
    title: 'Rental market analysis Dubai',
    query: 'Analyze the current rental market in Dubai by neighborhood. Compare prices in Marina, Downtown, Palm Jumeirah, and Business Bay. Include trends and investment opportunities.',
    icon: <BarChart3 className="text-green-700 dark:text-green-400" size={16} />,
  },
  {
    title: 'List property for rent',
    query: 'Help me create a professional listing for my 3-bedroom villa in Palm Jumeirah. Generate compelling description, set competitive pricing, and suggest the best rental platforms for Dubai market.',
    icon: <PenTool className="text-rose-700 dark:text-rose-400" size={16} />,
  },
  {
    title: 'Short-term rental investment',
    query: 'Analyze potential ROI for buying a property in Dubai for Airbnb. Include market research, estimated occupancy rates, monthly revenue projections, and Dubai tourism trends.',
    icon: <TrendingUp className="text-purple-700 dark:text-purple-400" size={16} />,
  },
  {
    title: 'Rental application assistant',
    query: 'Help me prepare a strong rental application for a luxury apartment in Downtown Dubai. Include required documents, references, and tips to stand out to landlords in the UAE market.',
    icon: <FileText className="text-orange-700 dark:text-orange-400" size={16} />,
  },
  {
    title: 'Property viewing scheduler',
    query: 'Coordinate viewing appointments for 5 apartments in Dubai this weekend. Send confirmation emails to landlords and create an optimized viewing route across different neighborhoods.',
    icon: <Calendar className="text-indigo-700 dark:text-indigo-400" size={16} />,
  },
  {
    title: 'Lease negotiation help',
    query: 'Help me negotiate better terms for a 1-year lease in Dubai. Suggest reasonable requests for rent reduction, pet policy, and lease flexibility according to UAE rental laws.',
    icon: <DollarSign className="text-cyan-700 dark:text-cyan-400" size={16} />,
  },
  {
    title: 'Property damage assessment',
    query: 'Document and assess rental property damage after tenant move-out in Dubai. Create detailed report with photos and estimated repair costs for security deposit deduction according to UAE law.',
    icon: <Shield className="text-teal-700 dark:text-teal-400" size={16} />,
  },
  {
    title: 'Airbnb listing optimization',
    query: 'Optimize my Dubai Airbnb listing to increase bookings. Improve photos, description, pricing strategy, and guest communication templates for the Middle East market.',
    icon: <Star className="text-violet-700 dark:text-violet-400" size={16} />,
  },
  {
    title: 'Tenant screening process',
    query: 'Create a comprehensive tenant screening checklist for Dubai including credit checks, references, employment verification, and legal compliance requirements according to UAE regulations.',
    icon: <Users className="text-red-700 dark:text-red-400" size={16} />,
  },
  {
    title: 'Corporate housing search',
    query: 'Find short-term corporate housing in Dubai for 30 days. Fully furnished, near DIFC, with business amenities and flexible check-in for international executives.',
    icon: <Briefcase className="text-pink-700 dark:text-pink-400" size={16} />,
  },
  {
    title: 'Rental property maintenance',
    query: 'Schedule quarterly maintenance for my Dubai rental properties. Coordinate HVAC service, pest control, and safety inspections. Track costs and create reports for property management.',
    icon: <Settings className="text-blue-600 dark:text-blue-300" size={16} />,
  },
  {
    title: 'Guest check-in automation',
    query: 'Create an automated check-in system for my Dubai vacation rental. Include keyless entry instructions, house rules, and emergency contacts for international guests.',
    icon: <Key className="text-red-600 dark:text-red-300" size={16} />,
  },
  {
    title: 'Rental income tracking',
    query: 'Set up a system to track rental income, expenses, and tax deductions for Dubai properties. Include rent collection, maintenance costs, and quarterly reports for UAE tax compliance.',
    icon: <Target className="text-amber-700 dark:text-amber-400" size={16} />,
  },
  {
    title: 'Property photo shoot',
    query: 'Plan a professional photo shoot for my Dubai rental listing. Schedule photographer, stage the property, and create a shot list highlighting key features for the luxury market.',
    icon: <Camera className="text-yellow-600 dark:text-yellow-300" size={16} />,
  },
  {
    title: 'Neighborhood guide creation',
    query: 'Create a comprehensive neighborhood guide for my Dubai rental guests. Include restaurants, attractions, transportation, and local recommendations for Marina, Downtown, and Palm areas.',
    icon: <MapPin className="text-orange-600 dark:text-orange-300" size={16} />,
  },
  {
    title: 'Rental price analysis',
    query: 'Analyze current market rates for similar properties in Dubai. Suggest optimal pricing strategy for maximum occupancy and revenue in the UAE rental market.',
    icon: <Zap className="text-slate-700 dark:text-slate-400" size={16} />,
  },
  {
    title: 'Student housing search',
    query: 'Help international student find affordable housing near Dubai universities. Include roommate matching, lease terms, and proximity to educational facilities.',
    icon: <Brain className="text-stone-700 dark:text-stone-400" size={16} />,
  },
  {
    title: 'Property investment calculator',
    query: 'Calculate potential returns on a Dubai rental property investment. Include purchase price, renovation costs, monthly expenses, and break-even analysis for UAE market.',
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