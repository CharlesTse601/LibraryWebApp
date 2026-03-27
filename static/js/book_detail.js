// book_detail.js — interactive behaviour for the book detail page

// Read values injected by the template via data attributes
const scriptTag   = document.currentScript;
const csrfToken   = scriptTag.dataset.csrf;
const userVotes   = JSON.parse(scriptTag.dataset.votes || '{}');

document.addEventListener('DOMContentLoaded', () => {
  // Restore active vote state from previous session
  Object.entries(userVotes).forEach(([id, type]) => {
    const btn = document.getElementById(`${type}-btn-${id}`);
    if (btn) btn.classList.add('active');
  });

  // Read more / read less toggle on review comments
  document.querySelectorAll('.bd-read-more').forEach(btn => {
    btn.addEventListener('click', function () {
      const comment = this.previousElementSibling;
      comment.classList.toggle('expanded');
      this.textContent = comment.classList.contains('expanded') ? 'Read less \u25b2' : 'Read more \u25bc';
    });
  });
});

// Submit a like / dislike vote via AJAX
function castVote(reviewId, voteType) {
  fetch(`/reviews/${reviewId}/vote/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `vote_type=${voteType}`,
  }).then(r => r.json()).then(data => {
    document.getElementById(`likes-${reviewId}`).textContent    = data.likes;
    document.getElementById(`dislikes-${reviewId}`).textContent = data.dislikes;
    const card = document.getElementById(`review-${reviewId}`);
    card.querySelectorAll('.bd-vote-btn').forEach(b => b.classList.remove('active'));
    if (data.user_vote) {
      const idx = data.user_vote === 'like' ? 0 : 1;
      card.querySelectorAll('.bd-vote-btn')[idx].classList.add('active');
    }
  });
}

// Generic AJAX POST helper
function ajaxPost(url, onSuccess) {
  fetch(url, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken, 'X-Requested-With': 'XMLHttpRequest' },
  }).then(r => r.json()).then(onSuccess);
}

// Add-to-list forms — submit via AJAX and disable button on success
document.querySelectorAll('form[action*="/add/"]').forEach(form => {
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    ajaxPost(this.action, data => {
      if (data.success) {
        const btn = this.querySelector('button');
        btn.textContent = 'Added \u2713';
        btn.disabled = true;
      }
    });
  });
});

// Review submission — AJAX post, then prepend new card without a page reload
const reviewForm = document.getElementById('review-form');
if (reviewForm) {
  reviewForm.addEventListener('submit', function (e) {
    e.preventDefault();
    fetch(this.action, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken, 'X-Requested-With': 'XMLHttpRequest' },
      body: new FormData(this),
    }).then(r => r.json()).then(data => {
      if (data.success) {
        const list = document.getElementById('reviews-list');
        const noReviews = document.getElementById('no-reviews');
        if (noReviews) noReviews.remove();
        const stars = '\u2605'.repeat(parseInt(data.star_rating)) + '\u2606'.repeat(5 - parseInt(data.star_rating));
        const card = document.createElement('div');
        card.className = 'bd-review-card';
        card.innerHTML = `
          <div class="bd-review-card__avatar">&#9679;</div>
          <div class="bd-review-card__body">
            <div class="bd-review-card__meta">
              <a href="#" class="bd-review-card__username">${data.user}</a>
              <span class="bd-review-card__stars">${stars}</span>
            </div>
            <p class="bd-review-card__comment">${data.comment}</p>
            <button class="bd-read-more">Read more &#9660;</button>
          </div>
          <div class="bd-review-card__votes">
            <span class="bd-vote-static">&#9650; 0</span>
            <span class="bd-vote-static">&#9660; 0</span>
          </div>`;
        list.prepend(card);
        reviewForm.reset();
        document.getElementById('review-form-panel').classList.remove('open');
      }
    });
  });
}
