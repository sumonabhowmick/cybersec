import {useCallback,useState} from 'react';

export function useApi(action){
  const [loading,setLoading]=useState(false);const [error,setError]=useState('');
  const run=useCallback(async(...args)=>{setLoading(true);setError('');try{return await action(...args)}catch(err){setError(err.message||'Request failed');throw err}finally{setLoading(false)}},[action]);
  return {run,loading,error};
}
