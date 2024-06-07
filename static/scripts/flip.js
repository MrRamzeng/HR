// import { PageFlip } from 'page-flip';
  const pageFlip = new St.PageFlip(document.getElementById('book'), {
    width: bookWidth, // required parameter - base page width
    height: bookHeight, // required parameter - base page height
    drawShadow: true,
    // size: "stretch",
    autoSize: false,
    mobileScrollSupport: true,
    showCover: true,
  });
  pageFlip.loadFromHTML(document.querySelectorAll('.page'));