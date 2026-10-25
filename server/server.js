const express = require('express');
const cors = require('cors');
const path = require('path');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const db = require('./db');

const app = express();
const PORT = process.env.PORT || 5000;
const JWT_SECRET = 'airbnb_secret_super_key_2026';

app.use(cors());
app.use(express.json());

// Helper DB queries as promises
const runQuery = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function (err) {
      if (err) reject(err);
      else resolve(this);
    });
  });
};

const getRow = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) reject(err);
      else resolve(row);
    });
  });
};

const getAllRows = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
};

// ==========================================
// 1. AUTHENTICATION APIS (S01, S02)
// ==========================================

// Register (S02)
app.post('/api/v1/auth/register', async (req, res) => {
  try {
    const { full_name, email, password, phone, role } = req.body;

    if (!full_name || !email || !password) {
      return res.status(400).json({ error: 'Vui lòng nhập đầy đủ họ tên, email và mật khẩu!' });
    }

    const existing = await getRow('SELECT id FROM users WHERE email = ?', [email.trim().toLowerCase()]);
    if (existing) {
      return res.status(400).json({ error: 'Email này đã được đăng ký trên hệ thống!' });
    }

    const password_hash = await bcrypt.hash(password, 10);
    const userRole = role === 'host' ? 'host' : 'customer';
    const avatar_url =
      userRole === 'host'
        ? 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=300&q=80'
        : 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80';

    const result = await runQuery(
      `INSERT INTO users (full_name, email, password_hash, phone, avatar_url, role) 
       VALUES (?, ?, ?, ?, ?, ?)`,
      [full_name, email.trim().toLowerCase(), password_hash, phone || '', avatar_url, userRole]
    );

    const newUser = {
      id: result.lastID,
      full_name,
      email: email.trim().toLowerCase(),
      phone: phone || '',
      avatar_url,
      role: userRole,
    };

    const token = jwt.sign({ id: newUser.id, role: newUser.role }, JWT_SECRET, { expiresIn: '7d' });

    res.status(201).json({
      message: 'Đăng ký tài khoản thành công!',
      user: newUser,
      token,
    });
  } catch (err) {
    console.error('Register error:', err);
    res.status(500).json({ error: 'Lỗi server khi đăng ký tài khoản.' });
  }
});

// Login (S01)
app.post('/api/v1/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Vui lòng nhập email và mật khẩu!' });
    }

    const user = await getRow('SELECT * FROM users WHERE email = ?', [email.trim().toLowerCase()]);
    if (!user) {
      return res.status(401).json({ error: 'Email hoặc mật khẩu không chính xác!' });
    }

    const isMatch = await bcrypt.compare(password, user.password_hash);
    if (!isMatch) {
      return res.status(401).json({ error: 'Email hoặc mật khẩu không chính xác!' });
    }

    const userObj = {
      id: user.id,
      full_name: user.full_name,
      email: user.email,
      phone: user.phone,
      avatar_url: user.avatar_url,
      role: user.role, // 'customer' | 'host'
    };

    const token = jwt.sign({ id: user.id, role: user.role }, JWT_SECRET, { expiresIn: '7d' });

    res.json({
      message: 'Đăng nhập thành công!',
      user: userObj,
      token,
    });
  } catch (err) {
    console.error('Login error:', err);
    res.status(500).json({ error: 'Lỗi server khi đăng nhập.' });
  }
});

// Get Current User (GET /me)
app.get('/api/v1/auth/me', async (req, res) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader) return res.status(401).json({ error: 'Chưa đăng nhập' });

    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, JWT_SECRET);

    const user = await getRow('SELECT id, full_name, email, phone, avatar_url, role FROM users WHERE id = ?', [decoded.id]);
    if (!user) return res.status(404).json({ error: 'Người dùng không tồn tại' });

    res.json({ user });
  } catch (err) {
    res.status(401).json({ error: 'Phiên đăng nhập hết hạn hoặc không hợp lệ' });
  }
});

// ==========================================
// 2. LISTINGS APIS (C01, C02, C03, H02, H03)
// ==========================================

// Get listings with filters
app.get('/api/v1/listings', async (req, res) => {
  try {
    const rows = await getAllRows('SELECT * FROM listings ORDER BY is_featured DESC, id DESC');
    
    // Parse json columns
    const listings = rows.map((r) => ({
      ...r,
      images: r.images ? JSON.parse(r.images) : [r.cover_image],
      amenities: r.amenities ? JSON.parse(r.amenities) : [],
      host: {
        id: r.host_id,
        name: r.host_id === 1 ? 'Lê Minh Thảo' : 'Nguyễn Văn An',
        avatar: r.host_id === 1 
          ? 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=300&q=80'
          : 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80',
        isSuperhost: true,
      }
    }));

    res.json({ data: listings });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Không thể tải danh sách chỗ ở.' });
  }
});

// Create new listing (Host UC-05)
app.post('/api/v1/listings', async (req, res) => {
  try {
    const {
      host_id,
      title,
      property_type,
      category,
      city,
      address,
      capacity,
      bedrooms,
      beds,
      baths,
      base_price,
      description,
      cover_image,
      images,
      amenities,
    } = req.body;

    const result = await runQuery(
      `INSERT INTO listings (
        host_id, title, property_type, category, city, address, capacity,
        bedrooms, beds, baths, base_price, status, cover_image, images,
        amenities, rating, reviews_count, description, is_featured
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Published', ?, ?, ?, 5.0, 0, ?, 0)`,
      [
        host_id || 1,
        title,
        property_type,
        category || 'nature',
        city,
        address,
        Number(capacity) || 2,
        Number(bedrooms) || 1,
        Number(beds) || 1,
        Number(baths) || 1,
        Number(base_price),
        cover_image,
        JSON.stringify(images || [cover_image]),
        JSON.stringify(amenities || []),
        description || '',
      ]
    );

    const created = await getRow('SELECT * FROM listings WHERE id = ?', [result.lastID]);
    res.status(201).json({
      message: 'Xuất bản chỗ ở thành công!',
      data: {
        ...created,
        images: JSON.parse(created.images),
        amenities: JSON.parse(created.amenities),
      },
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Lỗi khi tạo chỗ ở mới.' });
  }
});

// Toggle publish status (Published / Hidden)
app.patch('/api/v1/listings/:id/status', async (req, res) => {
  try {
    const { id } = req.params;
    const listing = await getRow('SELECT status FROM listings WHERE id = ?', [id]);
    if (!listing) return res.status(404).json({ error: 'Không tìm thấy chỗ ở' });

    const nextStatus = listing.status === 'Published' ? 'Hidden' : 'Published';
    await runQuery('UPDATE listings SET status = ? WHERE id = ?', [nextStatus, id]);

    res.json({ message: 'Cập nhật trạng thái thành công', status: nextStatus });
  } catch (err) {
    res.status(500).json({ error: 'Lỗi cập nhật trạng thái' });
  }
});

// ==========================================
// 3. BOOKINGS APIS (C04, C05, C07, H05)
// ==========================================

// Get bookings
app.get('/api/v1/bookings', async (req, res) => {
  try {
    const { customer_id, host_id } = req.query;
    let query = 'SELECT b.* FROM bookings b ORDER BY b.id DESC';
    let params = [];

    if (customer_id) {
      query = 'SELECT * FROM bookings WHERE customer_id = ? ORDER BY id DESC';
      params = [customer_id];
    } else if (host_id) {
      query = `SELECT b.* FROM bookings b 
               JOIN listings l ON b.listing_id = l.id 
               WHERE l.host_id = ? ORDER BY b.id DESC`;
      params = [host_id];
    }

    const rows = await getAllRows(query, params);
    const bookings = rows.map((r) => ({
      ...r,
      listing_snapshot: r.listing_snapshot ? JSON.parse(r.listing_snapshot) : {},
      reviewed: Boolean(r.reviewed),
    }));

    res.json({ data: bookings });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Không thể tải danh sách đơn đặt phòng.' });
  }
});

// Create Booking with double-booking check (BR-02)
app.post('/api/v1/bookings', async (req, res) => {
  try {
    const {
      listing_id,
      customer_id,
      check_in,
      check_out,
      guests,
      payment_method,
    } = req.body;

    const reqStart = new Date(check_in);
    const reqEnd = new Date(check_out);

    if (reqStart >= reqEnd) {
      return res.status(400).json({ error: 'Ngày trả phòng phải sau ngày nhận phòng!' });
    }

    // Check conflict with existing Confirmed bookings
    const conflictBooking = await getRow(
      `SELECT * FROM bookings 
       WHERE listing_id = ? AND status = 'Confirmed' 
       AND (check_in < ? AND check_out > ?)`,
      [listing_id, check_out, check_in]
    );

    if (conflictBooking) {
      return res.status(409).json({
        error: `Phòng đã có khách đặt từ ${conflictBooking.check_in} đến ${conflictBooking.check_out}!`,
      });
    }

    // Check conflict with host availability blocks
    const conflictBlock = await getRow(
      `SELECT * FROM availability_blocks 
       WHERE listing_id = ? 
       AND (start_date < ? AND end_date > ?)`,
      [listing_id, check_out, check_in]
    );

    if (conflictBlock) {
      return res.status(409).json({
        error: `Phòng bị chủ nhà tạm khóa từ ${conflictBlock.start_date} đến ${conflictBlock.end_date} (${conflictBlock.reason || 'Bảo trì'}).`,
      });
    }

    // Calculate nights & pricing
    const listing = await getRow('SELECT * FROM listings WHERE id = ?', [listing_id]);
    if (!listing) return res.status(404).json({ error: 'Không tìm thấy chỗ ở!' });

    const nights = Math.max(1, Math.round((reqEnd - reqStart) / (1000 * 60 * 60 * 24)));
    const unit_price = listing.base_price;
    const subtotal = nights * unit_price;
    const service_fee = Math.round(subtotal * 0.08);
    const tax = Math.round(subtotal * 0.08);
    const total = subtotal + service_fee + tax;

    const randomSuffix = Math.floor(100000 + Math.random() * 900000);
    const booking_code = `BK-2026-${randomSuffix}`;

    const listing_snapshot = JSON.stringify({
      title: listing.title,
      city: listing.city,
      address: listing.address,
      cover_image: listing.cover_image,
      host_name: 'Lê Minh Thảo',
    });

    const result = await runQuery(
      `INSERT INTO bookings (
        booking_code, listing_id, customer_id, check_in, check_out, guests,
        nights, unit_price, subtotal, service_fee, tax, total, currency,
        payment_method, status, listing_snapshot
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'VND', ?, 'Confirmed', ?)`,
      [
        booking_code,
        listing_id,
        customer_id || 2,
        check_in,
        check_out,
        Number(guests) || 1,
        nights,
        unit_price,
        subtotal,
        service_fee,
        tax,
        total,
        payment_method || 'vietqr',
        listing_snapshot,
      ]
    );

    const createdBooking = await getRow('SELECT * FROM bookings WHERE id = ?', [result.lastID]);

    res.status(201).json({
      message: 'Đặt phòng thành công!',
      booking: {
        ...createdBooking,
        listing_snapshot: JSON.parse(createdBooking.listing_snapshot),
      },
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Lỗi server khi đặt phòng.' });
  }
});

// Cancel booking (UC-04)
app.post('/api/v1/bookings/:id/cancel', async (req, res) => {
  try {
    const { id } = req.params;
    const { reason } = req.body;

    await runQuery(
      `UPDATE bookings 
       SET status = 'Cancelled', cancellation_reason = ? 
       WHERE id = ?`,
      [reason || 'Thay đổi lịch trình cá nhân', id]
    );

    res.json({ message: 'Đã hủy đặt phòng thành công. Lịch đã được giải phóng!' });
  } catch (err) {
    res.status(500).json({ error: 'Lỗi khi hủy đặt phòng.' });
  }
});

// ==========================================
// 4. REVIEWS APIS (C11 / UC-08)
// ==========================================
app.get('/api/v1/reviews', async (req, res) => {
  try {
    const { listing_id } = req.query;
    let query = 'SELECT * FROM reviews ORDER BY id DESC';
    let params = [];
    if (listing_id) {
      query = 'SELECT * FROM reviews WHERE listing_id = ? ORDER BY id DESC';
      params = [listing_id];
    }
    const reviews = await getAllRows(query, params);
    res.json({ data: reviews });
  } catch (err) {
    res.status(500).json({ error: 'Không thể tải đánh giá' });
  }
});

app.post('/api/v1/reviews', async (req, res) => {
  try {
    const { booking_id, listing_id, customer_id, author, avatar, rating, comment } = req.body;

    await runQuery(
      `INSERT INTO reviews (booking_id, listing_id, customer_id, author, avatar, rating, comment)
       VALUES (?, ?, ?, ?, ?, ?, ?)`,
      [booking_id, listing_id, customer_id || 2, author, avatar, Number(rating), comment]
    );

    if (booking_id) {
      await runQuery('UPDATE bookings SET reviewed = 1 WHERE id = ?', [booking_id]);
    }

    // Recalculate listing rating
    const revs = await getAllRows('SELECT rating FROM reviews WHERE listing_id = ?', [listing_id]);
    if (revs.length > 0) {
      const avg = (revs.reduce((sum, r) => sum + r.rating, 0) / revs.length).toFixed(2);
      await runQuery('UPDATE listings SET rating = ?, reviews_count = ? WHERE id = ?', [avg, revs.length, listing_id]);
    }

    res.status(201).json({ message: 'Gửi đánh giá thành công!' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Lỗi khi lưu đánh giá.' });
  }
});

// ==========================================
// 5. AVAILABILITY BLOCKS (Host H07 / UC-06)
// ==========================================
app.get('/api/v1/availability/blocks', async (req, res) => {
  try {
    const { listing_id } = req.query;
    let query = 'SELECT * FROM availability_blocks ORDER BY id DESC';
    let params = [];
    if (listing_id) {
      query = 'SELECT * FROM availability_blocks WHERE listing_id = ? ORDER BY id DESC';
      params = [listing_id];
    }
    const blocks = await getAllRows(query, params);
    res.json({ data: blocks });
  } catch (err) {
    res.status(500).json({ error: 'Lỗi lấy lịch chặn' });
  }
});

app.post('/api/v1/availability/block', async (req, res) => {
  try {
    const { listing_id, start_date, end_date, reason } = req.body;

    // Check if conflicting with confirmed bookings
    const conflict = await getRow(
      `SELECT * FROM bookings 
       WHERE listing_id = ? AND status = 'Confirmed'
       AND (check_in < ? AND check_out > ?)`,
      [listing_id, end_date, start_date]
    );

    if (conflict) {
      return res.status(409).json({
        error: `Không thể chặn ngày vì đã có đơn ${conflict.booking_code} của khách (${conflict.check_in} -> ${conflict.check_out})!`,
      });
    }

    const result = await runQuery(
      `INSERT INTO availability_blocks (listing_id, start_date, end_date, reason)
       VALUES (?, ?, ?, ?)`,
      [listing_id, start_date, end_date, reason || 'Chủ nhà tạm đóng']
    );

    const block = await getRow('SELECT * FROM availability_blocks WHERE id = ?', [result.lastID]);
    res.status(201).json({ message: 'Chặn ngày thành công', data: block });
  } catch (err) {
    res.status(500).json({ error: 'Lỗi khi chặn ngày' });
  }
});

app.delete('/api/v1/availability/block/:id', async (req, res) => {
  try {
    const { id } = req.params;
    await runQuery('DELETE FROM availability_blocks WHERE id = ?', [id]);
    res.json({ message: 'Đã mở lại ngày trên lịch' });
  } catch (err) {
    res.status(500).json({ error: 'Lỗi khi mở lại ngày' });
  }
});

// Serve Static Frontend Build (For single-service Hosting deployment)
const frontendDist = path.join(__dirname, '../frontend/dist');
app.use(express.static(frontendDist));

app.use((req, res) => {
  if (req.path.startsWith('/api/')) {
    return res.status(404).json({ error: 'Endpoint API không tồn tại' });
  }
  res.sendFile(path.join(frontendDist, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Backend REST API & Frontend server running with SQLite DB on http://127.0.0.1:${PORT}`);
});
