$(function(){
  //Simplicity vars
  var e = Explore;
  var m = DS.Model;
  var a = DS.attr;

  //Models
  e.PropertyMeta = m.extend({
    name: a('string'),
    reviews: a('number')
  });

  e.PropertyStatus = m.extend({
    yelp: a('boolean'),
    topics: a('boolean'),
    ready: function(){
      if(this.get('yelp') && this.get('topics')){ return true; }
      else { return false; }
    }.property('yelp', 'topics')
  });

  e.Review = m.extend({
    text: a('string'),
    date: a('string'),
    show: false,
    timestamp: a('number'),
    noTopicsDisplayText: function(){
      var tmpArr = this.get('text').match( /[^\.!\?]+[\.!\?]+/g );
      //RETURN SHIT BUT FADE OUT YO.
    }.property('text'),
    displayText: function(){
      var ren = new RegExp("\n", "g");
      return this.get('text').replace(ren, "<br>");
    }.property('text'),
    displayReviews: [],
    grade: a('number'),
    colorGrade: function(){
      var colors = ['#601e00', '#803e00', '#a05e00', '#c07e06', '#e09e26'];
      var grade = this.get('grade');
      return "color: " + colors[grade-1];
    }.property('grade'),
    htmlGrade: function(){
      var grade = this.get('grade');
      var html = "";
      while(grade>0){
        html += "<i class='fa fa-star'></i> ";
        grade--;
      }
      return html;
    }.property('grade')
  });

  e.Topic = m.extend({
    name: a('string'),
    reviews: DS.hasMany('review'),
    selected: false,
    averageScore: function(){
      var score = 0;
      var num = 0;
      this.get('reviews').forEach(function(r){
        score += r.get('grade');
        num++;
      });
      score = score / num;
      return score;
    }.property('reviews'),
    averageScoreHtml: function(){
      var score = this.get('averageScore');
      var html = "";
      while(score>0.5){
        html += "<i class='fa fa-star'></i> ";
        score--;
      }
      if(score>0){
        html += "<i class='fa fa-star-half'></i> ";
      }
      return html;
    }.property('averageScore'),
  });

  e.Property = m.extend({
    name: a('string'),
    allSelected: true,
    numSelected: function(){
      var count = 0;
      if(this.get('allSelected')){return "All";}
      this.get('topics').forEach(function(t){if(t.get('selected')){count++;}});
      return count;
    }.property('allSelected', 'topics.@each.selected'),
    anyFilter: true,
    reviews: DS.hasMany('review'),
    topics: DS.hasMany('topic'),
    sortedTopics: function(){
      return this.get('topics').sortBy('reviews.length').reverse();
    }.property('@each.topics'),
    filteredReviews: function(){
      if(this.get('allSelected')){return this.get('reviews');}
      else if(this.get('anyFilter')){
        var revs = [];
        this.get('topics').forEach(function(t){
          t.get('reviews').forEach(function(r){
            if(t.get('selected')){
              var found = false;
              revs.forEach(function(e){
                if(r.get('id') == e.get('id')){found = true;}
              });
              if(!found){revs.pushObject(r);}
            }
          });
        });
        return revs;
      }else{
        topix = [];
        this.get('topics').forEach(function(t){if(t.get('selected')){topix.pushObject(t);}});
        console.log(topix);
        var revs = topix[0].get('reviews');
        topix.forEach(function(t){
          var newRevs = [];
          t.get('reviews').forEach(function(tr){
            revs.forEach(function(r){
              if(r.get('id') == tr.get('id')){newRevs.pushObject(r);}
            });
          });
          revs = newRevs;
        });
        return revs;
      }
    }.property('topics.@each.selected', 'allSelected', 'anyFilter', 'reviews'),
    sortedReviews: function(){
      return this.get('reviews').sortBy('grade').reverse();
    }.property('reviews'),
    filteredSortedReviews: function(){
      var self = this;
      var revs = this.get('filteredReviews').sortBy('timestamp').reverse();
      var rev = "";
      revs.forEach(function(r){
        rev = r.get('text');
        self.get('topics').forEach(function(t){
          if(t.get('selected') == true || self.get('allSelected') == true){
            var re = new RegExp(t.get('name'), "gi");
            rev = rev.replace(re, '<strong class="color-orange">' + t.get('name') + '</strong>');
          } else {
            var re = new RegExp('<strong class="color-orange">' + t.get('name') + '</strong>', "gi");
            rev = rev.replace(re, t.get('name'));
          }
        });
        var ren = new RegExp("\n", "g");
        rev = rev.replace(ren, "<br>");
        var pointsArr = [];
        var tmpArr = rev.match( /[^\.!\?]+[\.!\?]+/g );
        if(tmpArr){
          tmpArr.forEach(function(s){
            ren = new RegExp("<br>", "g");
            if(s.indexOf('<strong ') != -1){
              s = s.replace(ren, " ");
              pointsArr.pushObject(s);
            }
          });
        }
        
        r.set('displayReviews', pointsArr);
      });
      return revs;
    }.property('filteredReviews'),
    averageScore: function(){
      var score = 0;
      var num = 0;
      this.get('reviews').forEach(function(r){
        score += r.get('grade');
        num++;
      });
      score = score / num;
      return score;
    }.property('reviews'),
    averageScoreHtml: function(){
      var score = this.get('averageScore');
      var html = "";
      while(score>0.5){
        html += "<i class='fa fa-star'></i> ";
        score--;
      }
      if(score>0){
        html += "<i class='fa fa-star-half'></i> ";
      }
      return html;
    }.property('averageScore'),
    averageFilteredScore: function(){
      var score = 0;
      var num = 0;
      this.get('filteredReviews').forEach(function(r){
        score += r.get('grade');
        num++;
      });
      score = score / num;
      return score;
    }.property('filteredReviews'),
    averageFilteredScoreHtml: function(){
      var score = this.get('averageFilteredScore');
      var html = "";
      while(score>0.5){
        html += "<i class='fa fa-star'></i> ";
        score--;
      }
      if(score>0){
        html += "<i class='fa fa-star-half'></i> ";
      }
      return html;
    }.property('averageFilteredScore'),
    distributions: function(){
      var total = 0;
      var dists = [
        {
          score: "5 star",
          grade: 5,
          num: 0,
          style: "width: 0;"
        },
        {
          score: "4 star",
          grade: 4,
          num: 0,
          style: "width: 0;"
        },
        {
          score: "3 star",
          grade: 3,
          num: 0,
          style: "width: 0;"
        },
        {
          score: "2 star",
          grade: 2,
          num: 0,
          style: "width: 0;"
        },
        {
          score: "1 star",
          grade: 1,
          num: 0,
          style: "width: 0;"
        }
      ];
      this.get('filteredReviews').forEach(function(r){
        dists.forEach(function(d){if(r.get('grade') == d.grade){d.num++;}});
        total++;
      });
      dists.forEach(function(d){d.style = 'width: ' + ((d.num / total) * 100) + '%';});
      return dists;
    }.property('filteredReviews'),
    bestReview: function(){
      return this.get('sortedReviews')[0];
    }.property('@each.reviews'),
    worstReview: function(){
      return this.get('sortedReviews')[this.get('sortedReviews').length-1];
    }.property('@each.reviews')
  });
});
