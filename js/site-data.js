/* ==========================================================================
   SPICE ROUTE — SITE CONFIGURATION
   --------------------------------------------------------------------------
   THIS IS THE ONLY FILE YOU NEED TO EDIT FOR MOST BUSINESS DETAILS.
   Change a value here and it updates every page of the website automatically
   (phone numbers, WhatsApp links, e-mail, address, opening hours, socials).

   HOW IT WORKS
   Every page contains normal, static HTML for search engines and for users
   with JavaScript disabled. Those static values are then "hydrated" from this
   file by js/script.js, so this file always wins when it is loaded.

   Anything in the markup like  data-site-field="phone"  is replaced with the
   matching value below. See README.md → "Making client edits".
   ========================================================================== */

window.SITE = {
  /* ------------------------------------------------------------------
     1. IDENTITY
     ------------------------------------------------------------------ */
  name: 'Spice Route',
  tagline: 'Authentic Indian Flavours, Served With Soul',
  shortDescription:
    'Charcoal-smoked tandoor cooking, hand-ground masala and slow-simmered gravies — served in a warm, lantern-lit dining room in the heart of the city.',

  founded: '2014',

  /* ------------------------------------------------------------------
     2. CONTACT DETAILS
     Replace the demo values below with the real ones.
     ------------------------------------------------------------------ */
  phoneDisplay: '+91 98765 43210',      // how the number is shown to visitors
  phoneDial: '+919876543210',          // digits only, used by tel: links

  whatsappNumber: '919876543210',       // country code + number, digits only
  whatsappMessage:
    'Hello Spice Route! I would like to ask about a table reservation.',

  email: 'hello@spiceroute.example',

  address: {
    line1: '42, Saffron Street',
    line2: 'Brigade Road, Indiranagar',
    city: 'Bengaluru',
    region: 'Karnataka',
    postcode: '560038',
    country: 'India',
    // One-line version used in the footer and on the contact page
    oneLine: '42, Saffron Street, Brigade Road, Indiranagar, Bengaluru 560038',
    // Coordinates (used by the map link and the Restaurant schema)
    lat: 12.97194,
    lng: 77.64123
  },

  /* ------------------------------------------------------------------
     3. OPENING HOURS
     `closed: true` hides the day from the contact page hours table.
     `note` is optional and shows underneath the day.
     ------------------------------------------------------------------ */
  hours: [
    { days: 'Monday – Thursday', open: '12:00 pm', close: '10:30 pm', closed: false },
    { days: 'Friday – Saturday', open: '12:00 pm', close: '11:30 pm', closed: false },
    { days: 'Sunday', open: '12:00 pm', close: '10:00 pm', closed: false }
  ],
  hoursNote: 'Kitchen closes 30 minutes before the restaurant. Walk-ins are always welcome, but we recommend booking at weekends.',
  // Used by the Restaurant structured data (schema.org)
  schemaHours: ['Mo-Th 12:00-22:30', 'Fr-Sa 12:00-23:30', 'Su 12:00-22:00'],

  /* ------------------------------------------------------------------
     4. SOCIAL LINKS
     Set a link to '' to hide that icon everywhere on the site.
     ------------------------------------------------------------------ */
  social: {
    instagram: 'https://www.instagram.com/',
    facebook: 'https://www.facebook.com/',
    x: 'https://x.com/',
    tripadvisor: 'https://www.tripadvisor.com/'
  },

  /* ------------------------------------------------------------------
     5. LOCATION LINKS
     ------------------------------------------------------------------ */
  // Swap for your own Google Maps place URL once the restaurant is live:
  // https://www.google.com/maps/place/<your-place-id>
  mapUrl:
    'https://www.google.com/maps/search/?api=1&query=' +
    encodeURIComponent('Brigade Road, Indiranagar, Bengaluru, Karnataka 560038'),

  /* ------------------------------------------------------------------
     6. SERVICE DETAILS (used on the contact page + schema.org)
     ------------------------------------------------------------------ */
  cuisine: ['North Indian', 'Mughlai', 'Awadhi', 'Hyderabadi', 'Indian Street Food'],
  priceRange: '₹₹',
  acceptsReservations: true,

  /* ------------------------------------------------------------------
     7. FOOTER / LEGAL
     ------------------------------------------------------------------ */
  copyright: '© ' + new Date().getFullYear() + ' Spice Route. All rights reserved.',
  // Because this is a portfolio demo, a short disclaimer is shown in the footer.
  disclaimer:
    'Spice Route is a fictional restaurant created as a web-design portfolio demo. Details, prices, reviews and photography are illustrative only.',

  /* ------------------------------------------------------------------
     8. MISC
     ------------------------------------------------------------------ */
  currency: '₹',
  bookingLeadTimeDays: 1,   // booking form will not allow a date in the past
  maxGuestsPerBooking: 12
};
