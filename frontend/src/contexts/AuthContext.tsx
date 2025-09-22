import React, { createContext, useContext, useEffect, useState } from 'react';
import { 
  GoogleAuthProvider, 
  signInWithPopup, 
  signOut, 
  onAuthStateChanged,
  User
} from 'firebase/auth';
import { auth } from '../firebase/config';

interface AuthContextType {
  currentUser: User | null;
  loading: boolean;
  signInWithGoogle: () => Promise<void>;
  logout: () => Promise<void>;
  isDemo: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isDemo, setIsDemo] = useState(false);

  useEffect(() => {
    // For development, always use demo mode and skip Firebase authentication
    console.log("Running in demo mode - bypassing Firebase authentication");
    setIsDemo(true);
    setCurrentUser({
      uid: 'demo-user',
      email: 'demo@driversfriend.com',
      displayName: 'Demo User',
      photoURL: null
    } as User);
    setLoading(false);
    
    // Uncomment below to enable real Firebase authentication
    /*
    try {
      const unsubscribe = onAuthStateChanged(auth, (user) => {
        setCurrentUser(user);
        setLoading(false);
      });
      return unsubscribe;
    } catch (error) {
      console.warn("Firebase auth not available, running in demo mode");
      setIsDemo(true);
      setCurrentUser({
        uid: 'demo-user',
        email: 'demo@example.com',
        displayName: 'Demo User',
        photoURL: null
      } as User);
      setLoading(false);
    }
    */
  }, []);

  const signInWithGoogle = async () => {
    if (isDemo) {
      console.log("Demo mode: Google sign-in simulated");
      return;
    }
    
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
    } catch (error) {
      console.error("Error signing in with Google", error);
    }
  };

  const logout = async () => {
    if (isDemo) {
      console.log("Demo mode: Logout simulated");
      return;
    }
    
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Error signing out", error);
    }
  };

  const value = {
    currentUser,
    loading,
    signInWithGoogle,
    logout,
    isDemo
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};