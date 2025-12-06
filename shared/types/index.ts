/**
 * Shared TypeScript types for SilentVoice
 */

export interface HandLandmark {
  x: number;
  y: number;
  z: number;
}

export interface PoseMessage {
  type: 'pose';
  data: HandLandmark[][];
}

export interface PredictionMessage {
  type: 'prediction';
  word: string;
  confidence: number;
}

export interface ErrorMessage {
  type: 'error';
  message: string;
  error?: string;
}

export type WebSocketMessage = PoseMessage | PredictionMessage | ErrorMessage;

export interface TrainingSample {
  gesture: string;
  landmarks: number[][];
  timestamp: number;
  metadata?: {
    confidence?: number;
    handCount?: number;
    [key: string]: any;
  };
}

export type GestureType = 
  | 'HELLO'
  | 'YES'
  | 'NO'
  | 'THANK_YOU'
  | 'PLEASE'
  | 'SORRY'
  | 'GOOD'
  | 'BAD'
  | 'LOVE'
  | 'PEACE'
  | 'GOODBYE'
  | 'WELCOME'
  | 'HELP'
  | 'STOP'
  | 'GO'
  | 'COME'
  | 'EAT'
  | 'DRINK'
  | 'SLEEP'
  | 'WAKE_UP';

export interface RecognitionResult {
  word: GestureType | string;
  confidence: number;
  timestamp: number;
}

export interface ConnectionStatus {
  status: 'connecting' | 'connected' | 'disconnected' | 'error';
  isConnected: boolean;
  error?: string;
}

