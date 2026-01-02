import { useEffect, useState, useCallback, useRef } from 'react'

type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error'

interface UseWebSocketOptions {
  reconnectInterval?: number
  maxReconnectAttempts?: number
  heartbeatInterval?: number
}

export function useWebSocketStable(
  url: string,
  options: UseWebSocketOptions = {}
) {
  const {
    reconnectInterval = 3000,
    maxReconnectAttempts = 10,
    heartbeatInterval = 30000
  } = options

  const [lastMessage, setLastMessage] = useState<string | null>(null)
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('disconnected')
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()
  const heartbeatIntervalRef = useRef<NodeJS.Timeout>()
  const reconnectAttemptsRef = useRef(0)
  const shouldReconnectRef = useRef(true)
  const urlRef = useRef(url)

  urlRef.current = url

  const sendHeartbeat = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      try {
        wsRef.current.send(JSON.stringify({ type: 'ping' }))
      } catch (error) {
        console.error('Failed to send heartbeat:', error)
      }
    }
  }, [])

  const startHeartbeat = useCallback(() => {
    stopHeartbeat()
    heartbeatIntervalRef.current = setInterval(sendHeartbeat, heartbeatInterval)
  }, [sendHeartbeat, heartbeatInterval])

  const stopHeartbeat = useCallback(() => {
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current)
      heartbeatIntervalRef.current = undefined
    }
  }, [])

  const connect = useCallback(() => {
    if (!urlRef.current) {
      console.warn('WebSocket URL is empty')
      return
    }

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected')
      return
    }

    try {
      if (wsRef.current) {
        wsRef.current.close(1000, 'Reconnecting')
      }

      console.log(`Connecting to WebSocket: ${urlRef.current}`)
      setConnectionStatus('connecting')
      
      const ws = new WebSocket(urlRef.current)
      
      ws.onopen = () => {
        console.log('✅ WebSocket connected successfully')
        setConnectionStatus('connected')
        reconnectAttemptsRef.current = 0
        startHeartbeat()
        
        ws.send(JSON.stringify({ 
          type: 'connection',
          timestamp: Date.now()
        }))
      }
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          if (data.type !== 'pong') {
            setLastMessage(event.data)
          }
        } catch {
          setLastMessage(event.data)
        }
      }
      
      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
        setConnectionStatus('error')
      }
      
      ws.onclose = (event) => {
        console.log(`WebSocket closed: Code ${event.code}, Reason: ${event.reason || 'No reason'}`)
        setConnectionStatus('disconnected')
        stopHeartbeat()
        
        if (shouldReconnectRef.current && reconnectAttemptsRef.current < maxReconnectAttempts) {
          const delay = Math.min(reconnectInterval * Math.pow(1.5, reconnectAttemptsRef.current), 30000)
          console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttemptsRef.current + 1}/${maxReconnectAttempts})`)
          
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current++
            connect()
          }, delay)
        } else if (reconnectAttemptsRef.current >= maxReconnectAttempts) {
          console.error('Max reconnection attempts reached')
          setConnectionStatus('error')
        }
      }
      
      wsRef.current = ws
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
      setConnectionStatus('error')
    }
  }, [startHeartbeat, stopHeartbeat, reconnectInterval, maxReconnectAttempts])
  
  const disconnect = useCallback(() => {
    shouldReconnectRef.current = false
    stopHeartbeat()
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = undefined
    }
    
    if (wsRef.current) {
      wsRef.current.close(1000, 'Manual disconnect')
      wsRef.current = null
    }
    
    setConnectionStatus('disconnected')
    reconnectAttemptsRef.current = 0
  }, [stopHeartbeat])
  
  const sendMessage = useCallback((message: string) => {
    if (!wsRef.current) {
      console.warn('WebSocket not initialized')
      if (shouldReconnectRef.current) {
        connect()
      }
      return false
    }

    if (wsRef.current.readyState === WebSocket.CONNECTING) {
      console.log('WebSocket is connecting, queuing message...')
      setTimeout(() => sendMessage(message), 100)
      return false
    }

    if (wsRef.current.readyState === WebSocket.OPEN) {
      try {
        wsRef.current.send(message)
        return true
      } catch (error) {
        console.error('Failed to send message:', error)
        return false
      }
    }

    console.warn('WebSocket is not open, current state:', wsRef.current.readyState)
    return false
  }, [connect])
  
  useEffect(() => {
    shouldReconnectRef.current = true
    connect()
    
    const handleVisibilityChange = () => {
      if (document.hidden) {
        stopHeartbeat()
      } else if (wsRef.current?.readyState === WebSocket.OPEN) {
        startHeartbeat()
      }
    }

    const handleOnline = () => {
      console.log('Network online, reconnecting...')
      connect()
    }

    const handleOffline = () => {
      console.log('Network offline')
      setConnectionStatus('disconnected')
    }
    
    document.addEventListener('visibilitychange', handleVisibilityChange)
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    
    return () => {
      shouldReconnectRef.current = false
      document.removeEventListener('visibilitychange', handleVisibilityChange)
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
      disconnect()
    }
  }, [])
  
  return {
    lastMessage,
    sendMessage,
    connectionStatus,
    isConnected: connectionStatus === 'connected',
    connect,
    disconnect
  }
}
