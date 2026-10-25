const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const bcrypt = require('bcryptjs');

const dbPath = path.join(__dirname, 'database.sqlite');
const db = new sqlite3.Database(dbPath);

const { INITIAL_LISTINGS } = require('./seedData');

function initDatabase() {
  db.serialize(async () => {
    // 1. Users Table
    db.run(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        phone TEXT,
        avatar_url TEXT,
        role TEXT NOT NULL DEFAULT 'customer',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // 2. Listings Table
    db.run(`
      CREATE TABLE IF NOT EXISTS listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        host_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        property_type TEXT NOT NULL,
        category TEXT NOT NULL,
        city TEXT NOT NULL,
        address TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        bedrooms INTEGER DEFAULT 1,
        beds INTEGER DEFAULT 1,
        baths INTEGER DEFAULT 1,
        base_price INTEGER NOT NULL,
        status TEXT DEFAULT 'Published',
        cover_image TEXT,
        images TEXT,
        amenities TEXT,
        rating REAL DEFAULT 5.0,
        reviews_count INTEGER DEFAULT 0,
        description TEXT,
        is_featured INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(host_id) REFERENCES users(id)
      )
    `);

    // 3. Bookings Table
    db.run(`
      CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_code TEXT UNIQUE NOT NULL,
        listing_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        check_in TEXT NOT NULL,
        check_out TEXT NOT NULL,
        guests INTEGER NOT NULL,
        nights INTEGER NOT NULL,
        unit_price INTEGER NOT NULL,
        subtotal INTEGER NOT NULL,
        service_fee INTEGER NOT NULL,
        tax INTEGER NOT NULL,
        total INTEGER NOT NULL,
        currency TEXT DEFAULT 'VND',
        payment_method TEXT NOT NULL,
        status TEXT DEFAULT 'Confirmed',
        listing_snapshot TEXT,
        reviewed INTEGER DEFAULT 0,
        cancellation_reason TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(listing_id) REFERENCES listings(id),
        FOREIGN KEY(customer_id) REFERENCES users(id)
      )
    `);

    // 4. Reviews Table
    db.run(`
      CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id INTEGER UNIQUE,
        listing_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        author TEXT NOT NULL,
        avatar TEXT,
        rating INTEGER NOT NULL,
        comment TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // 5. Availability Blocks Table (Host Chặn ngày - UC-06)
    db.run(`
      CREATE TABLE IF NOT EXISTS availability_blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        listing_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        reason TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // 6. Wishlist Table
    db.run(`
      CREATE TABLE IF NOT EXISTS wishlists (
        user_id INTEGER NOT NULL,
        listing_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, listing_id)
      )
    `);

    // 7. Messages Table
    db.run(`
      CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT NOT NULL,
        listing_id INTEGER NOT NULL,
        sender_id INTEGER NOT NULL,
        sender_role TEXT NOT NULL,
        text TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // SEED INITIAL USERS IF NOT EXISTS
    const hash = await bcrypt.hash('123456', 10);

    // Host Account
    db.get('SELECT id FROM users WHERE email = ?', ['host@gmail.com'], (err, row) => {
      if (!row) {
        db.run(
          `INSERT INTO users (full_name, email, password_hash, phone, avatar_url, role) 
           VALUES (?, ?, ?, ?, ?, ?)`,
          [
            'Lê Minh Thảo (Superhost)',
            'host@gmail.com',
            hash,
            '0987654321',
            'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=300&q=80',
            'host'
          ]
        );
      }
    });

    // Customer Account
    db.get('SELECT id FROM users WHERE email = ?', ['customer@gmail.com'], (err, row) => {
      if (!row) {
        db.run(
          `INSERT INTO users (full_name, email, password_hash, phone, avatar_url, role) 
           VALUES (?, ?, ?, ?, ?, ?)`,
          [
            'Nguyễn Văn An',
            'customer@gmail.com',
            hash,
            '0901234567',
            'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80',
            'customer'
          ]
        );
      }
    });

    // SEED 20 LISTINGS IF EMPTY
    db.get('SELECT COUNT(*) as count FROM listings', (err, row) => {
      if (row && row.count === 0) {
        console.log('Seeding 20 listings into SQLite Database...');
        const stmt = db.prepare(`
          INSERT INTO listings (
            id, host_id, title, property_type, category, city, address, capacity,
            bedrooms, beds, baths, base_price, status, cover_image, images,
            amenities, rating, reviews_count, description, is_featured
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `);

        for (const l of INITIAL_LISTINGS) {
          stmt.run([
            l.id,
            l.host_id === 1 ? 2 : 1, // map to host user id
            l.title,
            l.property_type,
            l.category,
            l.city,
            l.address,
            l.capacity,
            l.bedrooms || 2,
            l.beds || 2,
            l.baths || 1,
            l.base_price,
            l.status || 'Published',
            l.cover_image,
            JSON.stringify(l.images || [l.cover_image]),
            JSON.stringify(l.amenities || []),
            l.rating || 5.0,
            l.reviews_count || 0,
            l.description,
            l.is_featured ? 1 : 0
          ]);
        }
        stmt.finalize();

        // Seed some sample bookings
        db.run(`
          INSERT INTO bookings (
            booking_code, listing_id, customer_id, check_in, check_out, guests,
            nights, unit_price, subtotal, service_fee, tax, total, payment_method, status, listing_snapshot
          ) VALUES (
            'BK-2026-888999', 101, 2, '2026-11-15', '2026-11-18', 2,
            3, 1850000, 5550000, 444000, 444000, 6438000, 'vietqr', 'Confirmed',
            '{"title":"Mây Lang Thang Villa","city":"Đà Lạt","address":"Đường Khởi Nghĩa Bắc Sơn","cover_image":"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80"}'
          )
        `);

        // Seed sample review
        db.run(`
          INSERT INTO reviews (booking_id, listing_id, customer_id, author, avatar, rating, comment)
          VALUES (
            1, 101, 2, 'Hoàng Long',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80',
            5, 'Không gian cực kỳ yên tĩnh, view săn mây buổi sáng ngắm thung lũng đẹp mê hồn!'
          )
        `);
      }
    });

    console.log('SQLite Database schema initialized successfully at ' + dbPath);
  });
}

initDatabase();

module.exports = db;
