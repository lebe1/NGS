import express from 'express';
import fs from 'fs';
import path from 'path';
import Mustache from 'mustache';
import data from './data/data.js';

const app = express();
const port = 3000;

// Serve static assets (images, CSS, JS) from assets/
app.use(express.static(path.join(process.cwd(), 'assets')));

app.get('/', (req, res) => {
  const filePath = path.join(process.cwd(), 'views', 'main.html');
  fs.readFile(filePath, 'utf8', (err, template) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.status(404).send('main.html not found');
      } else {
        res.status(500).send('Server error');
      }
    } else {
      const output = Mustache.render(template, data);
      res.send(output);
    }
  });
});

app.get('/categories', (req, res) => {
  const filePath = path.join(process.cwd(), 'views', 'categories.html');
  fs.readFile(filePath, 'utf8', (err, template) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.status(404).send('categories.html not found');
      } else {
        res.status(500).send('Server error');
      }
    } else {
      const output = Mustache.render(template, data);
      res.send(output);
    }
  });
});

// Dynamic route for categories - handles all category pages with one route
app.get('/categories/:categoryName', (req, res) => {
  const categoryName = req.params.categoryName;
  
  // Find the category in the data
  const category = data.categories.find(c => c.id === categoryName);
  
  // Check if the requested category exists
  if (!category) {
    return res.status(404).send('Category not found');
  }
  
  const filePath = path.join(process.cwd(), 'views', 'category.html');
  fs.readFile(filePath, 'utf8', (err, template) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.status(404).send('category.html not found');
      } else {
        res.status(500).send('Server error');
      }
    } else {
      // Filter products for this category and format prices
      const products = category.products.map(product => ({
        ...product,
        price: `${product.price.EUR}€`
      }));
      
      // Prepare view data for Mustache
      const viewData = {
        ...data,
        category_name: category.name,
        product_number: products.length,
        products
      };
      
      const output = Mustache.render(template, viewData);
      res.setHeader('Content-Type', 'text/html');
      res.send(output);
    }
  });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});