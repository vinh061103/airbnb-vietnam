import React, { useState } from "react";
import { useApp } from "../context/AppContext";
import { AMENITIES_LIST } from "../data/initialData";
import {
  ArrowLeft,
  PlusCircle,
  Sparkles,
  Check,
  Building,
  Image as ImageIcon,
  DollarSign,
  MapPin,
} from "lucide-react";

export default function HostNewListing() {
  const { addListing, setCurrentView } = useApp();

  const [title, setTitle] = useState("");
  const [propertyType, setPropertyType] = useState("Căn hộ");
  const [category, setCategory] = useState("nature");
  const [city, setCity] = useState("Đà Lạt");
  const [address, setAddress] = useState("");
  const [capacity, setCapacity] = useState(4);
  const [bedrooms, setBedrooms] = useState(2);
  const [beds, setBeds] = useState(2);
  const [baths, setBaths] = useState(1);
  const [basePrice, setBasePrice] = useState(1200000);
  const [description, setDescription] = useState("");
  const [coverImage, setCoverImage] = useState(
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
  );
  const [selectedAmenities, setSelectedAmenities] = useState([
    "wifi",
    "ac",
    "kitchen",
    "tv",
  ]);

  const toggleAmenity = (id) => {
    setSelectedAmenities((prev) =>
      prev.includes(id) ? prev.filter((a) => a !== id) : [...prev, id]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!title.trim() || !address.trim()) {
      alert("Vui lòng nhập đầy đủ Tên phòng và Địa chỉ chi tiết!");
      return;
    }

    addListing({
      title,
      property_type: propertyType,
      category,
      city,
      address,
      capacity: Number(capacity),
      bedrooms: Number(bedrooms),
      beds: Number(beds),
      baths: Number(baths),
      base_price: Number(basePrice),
      description:
        description ||
        `Chỗ ở tiện nghi phong cách hiện đại tại ${city}. Đầy đủ trang thiết bị và dịch vụ lưu trú chuyên nghiệp.`,
      cover_image: coverImage,
      images: [
        coverImage,
        "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=800&q=80",
      ],
      amenities: selectedAmenities,
    });

    alert("Chúc mừng! Chỗ ở mới của bạn đã được xuất bản thành công.");
    setCurrentView("host-listings");
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <button
        onClick={() => setCurrentView("host-listings")}
        className="mb-4 inline-flex items-center gap-2 text-sm font-bold text-gray-700 hover:text-gray-900"
      >
        <ArrowLeft className="w-4 h-4" /> Quay lại danh sách chỗ ở
      </button>

      <div className="bg-white border border-gray-200 rounded-3xl p-6 sm:p-10 shadow-lg space-y-8">
        <div>
          <span className="text-xs font-bold text-[#FF385C] uppercase tracking-widest bg-rose-50 px-3 py-1 rounded-full">
            Biểu mẫu UC-05
          </span>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 mt-2">
            Đăng phòng / Chỗ ở mới lên Airbnb
          </h1>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">
            Điền đầy đủ các thông số để giới thiệu nơi ở của bạn tới hàng triệu du khách.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 text-xs sm:text-sm">
          {/* Section 1: Thông tin cơ bản */}
          <div className="space-y-4">
            <h3 className="text-base font-bold text-gray-900 flex items-center gap-2">
              <Building className="w-4 h-4 text-[#FF385C]" />
              1. Thông tin chỗ ở
            </h3>

            <div>
              <label className="font-bold text-gray-700 block mb-1">
                Tên tiêu đề chỗ ở *
              </label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Ví dụ: Pine Hill Villa Đà Lạt - Căn Biệt Thự Gỗ Ngắm Mây"
                className="w-full border border-gray-300 rounded-2xl px-4 py-3 outline-none focus:border-gray-900"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="font-bold text-gray-700 block mb-1">
                  Loại hình chỗ ở
                </label>
                <select
                  value={propertyType}
                  onChange={(e) => setPropertyType(e.target.value)}
                  className="w-full border border-gray-300 rounded-2xl px-3 py-3 outline-none focus:border-gray-900 bg-white"
                >
                  <option value="Căn hộ">Căn hộ chung cư</option>
                  <option value="Biệt thự">Biệt thự cao cấp</option>
                  <option value="Homestay">Homestay ấm cúng</option>
                  <option value="Bungalow">Bungalow gỗ</option>
                  <option value="Studio">Phòng Studio</option>
                  <option value="Nhà phố">Nhà phố nguyên căn</option>
                </select>
              </div>

              <div>
                <label className="font-bold text-gray-700 block mb-1">
                  Thành phố / Điểm đến
                </label>
                <select
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="w-full border border-gray-300 rounded-2xl px-3 py-3 outline-none focus:border-gray-900 bg-white"
                >
                  <option value="Đà Lạt">Đà Lạt</option>
                  <option value="Phú Quốc">Phú Quốc</option>
                  <option value="Hội An">Hội An</option>
                  <option value="Hồ Chí Minh">Hồ Chí Minh</option>
                  <option value="Sa Pa">Sa Pa</option>
                  <option value="Vũng Tàu">Vũng Tàu</option>
                  <option value="Hà Nội">Hà Nội</option>
                  <option value="Nha Trang">Nha Trang</option>
                </select>
              </div>

              <div>
                <label className="font-bold text-gray-700 block mb-1">
                  Danh mục trải nghiệm
                </label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full border border-gray-300 rounded-2xl px-3 py-3 outline-none focus:border-gray-900 bg-white"
                >
                  <option value="nature">Núi rừng & Thiên nhiên</option>
                  <option value="beach">Gần biển</option>
                  <option value="villa">Biệt thự cao cấp</option>
                  <option value="city">Trung tâm thành phố</option>
                  <option value="pool">Hồ bơi vô cực</option>
                  <option value="romantic">Cặp đôi & Lãng mạn</option>
                </select>
              </div>
            </div>

            <div>
              <label className="font-bold text-gray-700 block mb-1">
                Địa chỉ chi tiết *
              </label>
              <input
                type="text"
                required
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="Ví dụ: 15 Đặng Thái Thân, Phường 3, TP. Đà Lạt"
                className="w-full border border-gray-300 rounded-2xl px-4 py-3 outline-none focus:border-gray-900"
              />
            </div>
          </div>

          {/* Section 2: Sức chứa & Giá */}
          <div className="space-y-4 pt-4 border-t border-gray-100">
            <h3 className="text-base font-bold text-gray-900 flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-[#FF385C]" />
              2. Sức chứa & Giá mỗi đêm
            </h3>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div>
                <label className="font-bold text-gray-700 block mb-1">
                  Sức chứa (khách)
                </label>
                <input
                  type="number"
                  min="1"
                  max="30"
                  value={capacity}
                  onChange={(e) => setCapacity(e.target.value)}
                  className="w-full border border-gray-300 rounded-2xl px-3 py-3 outline-none focus:border-gray-900 font-bold"
                />
              </div>

              <div>
                <label className="font-bold text-gray-700 block mb-1">
                  Số phòng ngủ
                </label>
                <input
                  type="number"
                  min="1"
                  value={bedrooms}
                  onChange={(e) => setBedrooms(e.target.value)}
                  className="w-full border border-gray-300 rounded-2xl px-3 py-3 outline-none focus:border-gray-900 font-bold"
                />
              </div>

              <div>
                <label className="font-bold text-gray-700 block mb-1">Số giường</label>
                <input
                  type="number"
                  min="1"
                  value={beds}
                  onChange={(e) => setBeds(e.target.value)}
                  className="w-full border border-gray-300 rounded-2xl px-3 py-3 outline-none focus:border-gray-900 font-bold"
                />
              </div>

              <div>
                <label className="font-bold text-gray-700 block mb-1">
                  Số phòng tắm
                </label>
                <input
                  type="number"
                  min="1"
                  value={baths}
                  onChange={(e) => setBaths(e.target.value)}
                  className="w-full border border-gray-300 rounded-2xl px-3 py-3 outline-none focus:border-gray-900 font-bold"
                />
              </div>
            </div>

            <div>
              <label className="font-bold text-gray-700 block mb-1">
                Giá cơ bản mỗi đêm (VND) *
              </label>
              <input
                type="number"
                step="50000"
                min="100000"
                required
                value={basePrice}
                onChange={(e) => setBasePrice(e.target.value)}
                className="w-full border border-gray-300 rounded-2xl px-4 py-3 outline-none focus:border-gray-900 font-bold text-base text-[#FF385C]"
              />
            </div>
          </div>

          {/* Section 3: Tiện nghi */}
          <div className="space-y-4 pt-4 border-t border-gray-100">
            <h3 className="text-base font-bold text-gray-900 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#FF385C]" />
              3. Tiện nghi sẵn có
            </h3>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
              {AMENITIES_LIST.map((am) => {
                const checked = selectedAmenities.includes(am.id);
                return (
                  <button
                    type="button"
                    key={am.id}
                    onClick={() => toggleAmenity(am.id)}
                    className={`p-3 rounded-2xl border text-left font-semibold text-xs flex items-center justify-between transition-all ${
                      checked
                        ? "border-[#FF385C] bg-rose-50/60 text-[#FF385C]"
                        : "border-gray-200 text-gray-700 hover:border-gray-300"
                    }`}
                  >
                    <span>{am.name}</span>
                    {checked && <Check className="w-4 h-4 stroke-[3]" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Section 4: Ảnh & Mô tả */}
          <div className="space-y-4 pt-4 border-t border-gray-100">
            <h3 className="text-base font-bold text-gray-900 flex items-center gap-2">
              <ImageIcon className="w-4 h-4 text-[#FF385C]" />
              4. Hình ảnh & Mô tả
            </h3>

            <div>
              <label className="font-bold text-gray-700 block mb-1">
                Link URL ảnh bìa (Cover Image)
              </label>
              <input
                type="url"
                value={coverImage}
                onChange={(e) => setCoverImage(e.target.value)}
                className="w-full border border-gray-300 rounded-2xl px-4 py-3 outline-none focus:border-gray-900 text-xs"
              />
            </div>

            <div>
              <label className="font-bold text-gray-700 block mb-1">
                Mô tả chi tiết chỗ ở
              </label>
              <textarea
                rows="4"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Giới thiệu điểm độc đáo, quang cảnh xung quanh, các điểm tham quan gần đó..."
                className="w-full border border-gray-300 rounded-2xl p-4 outline-none focus:border-gray-900 text-xs sm:text-sm"
              />
            </div>
          </div>

          {/* Buttons */}
          <div className="pt-6 border-t border-gray-200 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={() => setCurrentView("host-listings")}
              className="px-6 py-3.5 border border-gray-300 rounded-2xl font-bold text-gray-700 hover:bg-gray-50 text-xs"
            >
              Hủy bỏ
            </button>
            <button
              type="submit"
              className="bg-gradient-to-r from-[#FF385C] to-[#E00B41] hover:opacity-95 text-white font-extrabold px-8 py-3.5 rounded-2xl text-xs sm:text-sm shadow-xl transition-all active:scale-95"
            >
              Xuất bản chỗ ở ngay (Published)
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
