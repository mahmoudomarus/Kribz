import useSWR, { SWRConfiguration } from 'swr';
import { createClient } from '@/lib/supabase/client';
import { GetAccountsResponse } from '@usebasejump/shared';
import { useAuth } from '@/components/AuthProvider';

export const useAccounts = (options?: SWRConfiguration) => {
  const supabaseClient = createClient();
  const { user, isLoading } = useAuth();
  
  return useSWR<GetAccountsResponse>(
    // Only fetch when user is authenticated and not loading
    !!supabaseClient && !!user && !isLoading ? ['accounts'] : null,
    async () => {
      const { data, error } = await supabaseClient.rpc('get_accounts');

      if (error) {
        throw new Error(error.message);
      }

      return data;
    },
    options,
  );
};
