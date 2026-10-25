import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import {
  MessageSquare,
  Send,
  User,
  MapPin,
  ExternalLink,
  Smile,
  Clock,
} from "lucide-react";

export default function Messages() {
  const {
    conversations,
    sendMessage,
    role,
    setSelectedListingId,
    setCurrentView,
  } = useApp();

  const [activeConvId, setActiveConvId] = useState(
    conversations[0]?.conversation_id || null
  );
  const [inputText, setInputText] = useState("");

  const activeConversation =
    conversations.find((c) => c.conversation_id === activeConvId) ||
    conversations[0];

  const handleSend = (e) => {
    e.preventDefault();
    if (!inputText.trim() || !activeConversation) return;

    sendMessage(activeConversation.conversation_id, inputText);
    setInputText("");
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-4">
        <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2">
          <MessageSquare className="w-8 h-8 text-[#FF385C]" />
          Hộp thư tin nhắn
        </h1>
        <p className="text-xs sm:text-sm text-gray-500 mt-1">
          Trao đổi trực tiếp giữa Khách và Chủ nhà về chuyến đi (C10 / H09)
        </p>
      </div>

      <div className="bg-white border border-gray-200 rounded-3xl shadow-lg overflow-hidden grid grid-cols-1 md:grid-cols-12 min-h-[580px]">
        {/* Left: Conversations list (4 cols) */}
        <div className="md:col-span-4 border-r border-gray-200 flex flex-col">
          <div className="p-4 border-b border-gray-100 bg-gray-50/70">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
              Cuộc trò chuyện ({conversations.length})
            </span>
          </div>

          <div className="divide-y divide-gray-100 overflow-y-auto flex-1">
            {conversations.map((conv) => {
              const isActive = conv.conversation_id === activeConvId;
              const lastMsg = conv.messages[conv.messages.length - 1];

              return (
                <div
                  key={conv.id}
                  onClick={() => setActiveConvId(conv.conversation_id)}
                  className={`p-4 cursor-pointer transition-colors flex items-center gap-3 ${
                    isActive ? "bg-rose-50/50" : "hover:bg-gray-50"
                  }`}
                >
                  <img
                    src={conv.listing_image || conv.host.avatar}
                    alt={conv.listing_title}
                    className="w-12 h-12 rounded-2xl object-cover shadow-sm flex-shrink-0"
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="font-bold text-gray-900 text-xs truncate">
                        {conv.host.name}
                      </p>
                      <span className="text-[10px] text-gray-400">
                        {lastMsg ? lastMsg.time.split(",")[0] : ""}
                      </span>
                    </div>
                    <p className="text-[11px] font-semibold text-[#FF385C] truncate">
                      {conv.listing_title}
                    </p>
                    <p className="text-xs text-gray-500 truncate mt-0.5">
                      {lastMsg ? lastMsg.text : "Chưa có tin nhắn"}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Chat details (8 cols) */}
        <div className="md:col-span-8 flex flex-col">
          {activeConversation ? (
            <>
              {/* Header */}
              <div className="p-4 border-b border-gray-200 flex items-center justify-between bg-white">
                <div className="flex items-center gap-3">
                  <img
                    src={activeConversation.host.avatar}
                    alt={activeConversation.host.name}
                    className="w-10 h-10 rounded-full object-cover border border-gray-200"
                  />
                  <div>
                    <h3 className="font-bold text-gray-900 text-sm">
                      {activeConversation.host.name}
                    </h3>
                    <p className="text-[11px] text-gray-500">
                      Chủ nhà • Phản hồi trong vòng vài phút
                    </p>
                  </div>
                </div>

                <button
                  onClick={() => {
                    setSelectedListingId(activeConversation.listing_id);
                    setCurrentView("room-detail");
                  }}
                  className="flex items-center gap-1.5 text-xs font-bold text-gray-700 hover:text-[#FF385C] bg-gray-50 px-3 py-1.5 rounded-xl border border-gray-200"
                >
                  <span>Xem chỗ ở</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Messages Area */}
              <div className="flex-1 p-5 overflow-y-auto space-y-4 bg-gray-50/40">
                {activeConversation.messages.map((m, idx) => {
                  const isMe =
                    (role === "customer" && m.sender === "me") ||
                    (role === "host" && m.sender === "host");

                  return (
                    <div
                      key={idx}
                      className={`flex flex-col ${
                        isMe ? "items-end" : "items-start"
                      }`}
                    >
                      <div
                        className={`max-w-md px-4 py-2.5 rounded-2xl text-xs sm:text-sm shadow-sm ${
                          isMe
                            ? "bg-[#FF385C] text-white rounded-br-none"
                            : "bg-white text-gray-800 border border-gray-200 rounded-bl-none"
                        }`}
                      >
                        {m.text}
                      </div>
                      <span className="text-[10px] text-gray-400 mt-1 px-1">
                        {m.time}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* Input Form */}
              <form
                onSubmit={handleSend}
                className="p-3 border-t border-gray-200 bg-white flex items-center gap-2"
              >
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Nhập nội dung tin nhắn gửi chủ nhà..."
                  className="flex-1 bg-gray-100 rounded-2xl px-4 py-3 text-xs sm:text-sm outline-none focus:bg-white focus:ring-1 focus:ring-gray-900 transition-all"
                />
                <button
                  type="submit"
                  disabled={!inputText.trim()}
                  className="bg-[#FF385C] hover:bg-[#E00B41] text-white p-3 rounded-2xl shadow-md disabled:opacity-40 transition-all flex items-center justify-center"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-gray-400 text-sm">
              Chọn một cuộc hội thoại bên trái để bắt đầu trò chuyện
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
