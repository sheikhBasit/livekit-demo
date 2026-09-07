import { useState, useEffect } from "react";
import { useRoomContext, useLocalParticipant } from "@livekit/components-react";

export default function HandRaise({ role, userName }: { role: string, userName: string }) {
  const room = useRoomContext();
  const { localParticipant } = useLocalParticipant();
  const [notifications, setNotifications] = useState<{ id: string, name: string, time: number }[]>([]);

  useEffect(() => {
    if (!room) return;

    const handleDataReceived = (payload: Uint8Array, participant?: any) => {
      const decoder = new TextDecoder();
      const message = decoder.decode(payload);
      
      try {
        const data = JSON.parse(message);
        if (data.type === "raise_hand") {
          const newNotif = {
            id: Math.random().toString(),
            name: data.name || (participant ? participant.identity : "A student"),
            time: Date.now()
          };
          setNotifications(prev => [...prev, newNotif]);
          
          // Auto clear after 5 seconds
          setTimeout(() => {
            setNotifications(prev => prev.filter(n => n.id !== newNotif.id));
          }, 5000);
        }
      } catch (e) {
        console.error("Failed to parse data channel message", e);
      }
    };

    room.on("dataReceived", handleDataReceived);
    return () => {
      room.off("dataReceived", handleDataReceived);
    };
  }, [room]);

  const handleRaiseHand = () => {
    if (!localParticipant) return;
    const data = JSON.stringify({ type: "raise_hand", name: userName });
    const encoder = new TextEncoder();
    // Publish to all participants (or we could target just the teacher, but broadcasting is fine for this demo)
    localParticipant.publishData(encoder.encode(data), { reliable: true });
    
    // Optimistic local UI feedback
    alert("Hand raised! The teacher has been notified.");
  };

  return (
    <>
      {/* Student: Raise Hand Button */}
      {role === "student" && (
        <button
          onClick={handleRaiseHand}
          style={{
            position: "absolute",
            bottom: 24,
            right: 24,
            zIndex: 9999,
            padding: "12px 24px",
            backgroundColor: "#ff9800",
            color: "white",
            border: "none",
            borderRadius: 8,
            cursor: "pointer",
            fontWeight: "bold",
            boxShadow: "0 4px 6px rgba(0,0,0,0.1)"
          }}
        >
          ✋ Raise Hand
        </button>
      )}

      {/* Teacher: Notifications Display */}
      {role === "teacher" && notifications.length > 0 && (
        <div style={{
          position: "absolute",
          top: 24,
          right: 24,
          zIndex: 9999,
          display: "flex",
          flexDirection: "column",
          gap: 8
        }}>
          {notifications.map(n => (
            <div key={n.id} style={{
              padding: "12px 24px",
              backgroundColor: "#2196f3",
              color: "white",
              borderRadius: 8,
              boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
              animation: "fadeIn 0.3s ease-in-out"
            }}>
              ✋ <strong>{n.name}</strong> raised their hand!
            </div>
          ))}
        </div>
      )}
    </>
  );
}
