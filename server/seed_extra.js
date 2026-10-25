const db = require('./db');
const { INITIAL_LISTINGS } = require('./seedData');

const newOnes = INITIAL_LISTINGS.filter((l) => l.id >= 121);
console.log(`Inserting ${newOnes.length} new listings into SQLite...`);

const stmt = db.prepare(`
  INSERT OR REPLACE INTO listings (
    id, host_id, title, property_type, category, city, address, capacity,
    bedrooms, beds, baths, base_price, status, cover_image, images,
    amenities, rating, reviews_count, description, is_featured
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

for (const l of newOnes) {
  stmt.run([
    l.id,
    l.host_id === 1 ? 2 : 1,
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
    l.is_featured ? 1 : 0,
  ]);
}

stmt.finalize(() => {
  db.get('SELECT COUNT(*) as count FROM listings', (err, row) => {
    console.log('Total listings in SQLite Database:', row?.count);
    process.exit(0);
  });
});
