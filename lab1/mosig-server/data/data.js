const data = {
  top_sells: [
    {
      name: 'Covid mask FFP 200',
      number: '38331937286',
      image: '/img/products/mask.jpg',
      url: '/categories/virus'
    },
    {
      name: 'Carrots',
      number: '32147552649',
      image: '/img/products/carrots.jpg',
      url: '/categories/vegetables'
    },
    {
      name: 'Romanesco broccoli',
      number: '69492',
      image: '/img/products/romanesco.jpg',
      url: '/categories/vegetables'
    },
    {
      name: 'Nutella',
      number: '879',
      image: '/img/products/nutella.jpg',
      url: '/boutique/rayon/junk_food'
    }
  ],
  categories: [
    {
      id: 'fruits',
      name: 'Fruits',
      image: '/img/categories/fruits.jpg',
      products: [
        {
          name: 'Peach',
          image: '/img/products/peach.jpg',
          price: {
            EUR: 2.84,
            CAD: 4.1,
            USD: 2.99,
            GBP: 2.46,
            PHP: 169.31,
            IDR: 46.643
          }
        }
      ]
    },
    {
      id: 'junk_food',
      name: 'Junk Food',
      image: '/img/categories/junk_food.jpg',
      products: [
        {
          name: 'Nutella',
          image: '/img/products/nutella.jpg',
          price: {
            EUR: 2.84,
            CAD: 4.1,
            USD: 2.99,
            GBP: 2.46,
            PHP: 169.31,
            IDR: 46.643
          }
        }
      ]
    },
    {
      id: 'vegetables',
      name: 'Vegetables',
      image: '/img/categories/legumes.jpg',
      products: [
        {
          name: 'Carrots',
          image: '/img/products/carrots.jpg',
          price: {
            EUR: 2.84,
            CAD: 4.1,
            USD: 2.99,
            GBP: 2.46,
            PHP: 169.31,
            IDR: 46.643
          }
        },
        {
          name: 'Romanesco brocoli',
          image: '/img/products/romanesco.jpg',
          price: {
            EUR: 2.84,
            CAD: 4.1,
            USD: 2.99,
            GBP: 2.46,
            PHP: 169.31,
            IDR: 46.643
          }
        }
      ]
    },
    {
      id: 'virus',
      name: 'Virus',
      image: '/img/categories/corona.jpg',
      products: [
        {
          name: 'Masque FFP 200',
          image: '/img/products/mask.jpg',
          price: {
            EUR: 2.84,
            CAD: 4.1,
            USD: 2.99,
            GBP: 2.46,
            PHP: 169.31,
            IDR: 46.643
          }
        }
      ]
    }
  ]
};

export default data;
