!function ($, _H, Em, d3, vg) {

  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });

  $('#ratings-affix').affix({
    offset: {
      top: 100
    , bottom: function () {
        return (this.bottom = $('.footer').outerHeight(true))
      }
    }
  })

  $(function(){

    window.Explore = Em.Application.create({
      LOG_TRANSITIONS: true,
      ENABLE_ALL_FEATURES: true,
      LOG_ACTIVE_GENERATION: true,
      LOG_VIEW_LOOKUPS: true
    });

    window.Explore.store = DS.Store.extend({
      adapter: DS.RESTAdapter
    });

    Explore.ResetScroll = Ember.Mixin.create({
      activate: function() {
        this._super();
        $('html,body').animate({
          scrollTop: 0
        }, 1000);
      }
    });

    Explore.Router.map(function() {
      this.resource('explore', {path: '/'}, function(){
      });
      this.resource('processing');
      this.resource('propertyStatus', {path: 'status/:propertyStatus_id'}, function(){
      });
      this.resource('properties', {path: 'properties'}, function(){
      });
      this.resource('property', {path: 'property/:property_id'}, function(){
        this.resource('reviews', {path: '/reviews'}, function(){
        });
        this.resource('review', {path: '/review/:review_id'}, function(){
        });
      });
    });

    Explore.ExploreIndexRoute = Em.Route.extend({
      actions: {
        submitUrl: function(){
          var self = this;
          var url = this.controllerFor('exploreIndex').get('yelpUrl');
          self.controllerFor('exploreIndex').set('checking', true);
          $.ajax({
            url: '/explore',
            data: {yelp_url: url},
            type: 'POST'
          }).success(function(resp){
            self.controllerFor('exploreIndex').set('checking', false);
            if(resp["property_id"]==-1){
              self.controllerFor('exploreIndex').set('badUrl', true);
              self.controllerFor('exploreIndex').set('yelpUrl', "");
            }else{
              self.controllerFor('exploreIndex').set('badUrl', false);
              var propertyPromise = self.store.find('propertyStatus', resp["property_id"]);
              propertyPromise.then(function(status){
                self.transitionTo('propertyStatus', status);
              });
            }
          });
        },
        loadProperty: function(property){
          var self = this;
          this.controllerFor('exploreIndex').set('badUrl', false);
          this.controllerFor('exploreIndex').set('checking', false);
          var propertyPromise = this.store.find('propertyStatus', property.get('id'));
          propertyPromise.then(function(status){
            self.transitionTo('propertyStatus', status);
          });
        }
      }
    });

    Explore.ExploreIndexController = Em.Controller.extend({
      yelpUrl: "",
      checking: false,
      badUrl: false,
      properties: function(){
        return this.store.findAll('propertyMeta');
      }.property(),
      actions: {},
    });

    Explore.PropertyStatusRoute = Em.Route.extend({
      setupController: function(controller, model){
        var self = this;
        function recurse() {
          model.reload().then(function(status){
            console.log("UPDATED");
            if(status.get('ready')){
              var propertyPromise = self.store.find('property', status.get('id'));
              propertyPromise.then(function(prop){
                $("html, body").animate({ scrollTop: 0 }, "slow");
                self.transitionTo('property.index', prop);
              });
            } else {
              setTimeout(recurse, 3000);
            }
          });
        }
        setTimeout(recurse, 3000);
      },
      actions: {
        openProperty: function(property){
          var self = this;
          var propertyPromise = self.store.find('property', property.get('id'));
          propertyPromise.then(function(prop){
            $("html, body").animate({ scrollTop: 0 }, "slow");
            self.transitionTo('property.index', prop);
          });
        }
      },
    });

    Explore.PropertyStatusController = Em.Controller.extend({
    });

    Explore.ProcessingRoute = Em.Route.extend({
      model: function(){},
      setupController: function(controller, model){
        var self = this;
        var propertyPromise = self.store.find('property', controller.get('property'));
        propertyPromise.then(function(prop){
          self.transitionTo('property.index', prop);
        });
      }
    });

    Explore.ProcessingController = Em.Controller.extend({
      queryParams: ['property'],
      dataset: null
    });

    Explore.PropertyIndexRoute = Em.Route.extend({
      actions: {
        selectTopic: function(topic, property){
          var x = topic.get('selected');
          var allFalse = true;
          topic.set('selected', !x);
          property.set('allSelected', false);
          property.get('topics').forEach(function(t){if(t.get('selected')){allFalse = false;}});
          if(allFalse){property.set('allSelected', true);} 
        },
        anyAll: function(property){
          var x = property.get('anyFilter');
          property.set('anyFilter', !x);
        },
        selectAllTopics: function(property){
          if(!property.get('allSelected')){
            property.get('topics').forEach(function(t){
              t.set('selected', false);
            });
            property.get('reviews').forEach(function(r){
              r.set('show', false);
            });
            property.set('allSelected', true);
          }
        },
        showFullReview: function(review, property){
          var x = review.get('show');
          review.set('show', !x);
          console.log(review.get('show'));
        },
      }
    });

    Explore.PropertyIndexController = Em.Controller.extend({
      init: function() {
        var view = this;
        var resizeHandler = function() {
          //view.rerender();
        };
        this.set('resizeHandler', resizeHandler);
          $(window).bind('resize', this.get('resizeHandler'));
        },
      willDestroy: function() {
        $(window).unbind('resize', this.get('resizeHandler'));
      },
    });

    Explore.VerticalBarChartComponent = Ember.Component.extend({
      classNames: ['animated', 'fadeInDown'],
      didInsertElement: function(){
        Ember.run.once(this, 'update');
      },
      updateContent: function(){
        Ember.run.once(this, 'update');
      }.observes('distributions'),
      update: function(){
        var self = this;
        var groups = this.get('data');
        var groupData = []
        groups.forEach(function(g){
          var xAxisLabel = g.grade;
          //var color = '#e09e26';
          var colors = ['#601e00', '#803e00', '#a05e00', '#c07e06', '#e09e26'];
          if (g.num != 0){groupData.push({x: xAxisLabel, y: g.num, color: colors[g.grade-1]});}
        });
        var padding = {top: 0, left: 0, bottom: 0, right: 0};
        var spec = {
          padding: padding,
          width: self.$().width(),
          height: 300,
          data: [{name : 'Scores', values: groupData, transform: [{type: "pie", value: "data.y"}]}],
          scales: [
            {name: 'r', type: 'ordinal', range: [150, 150], domain: {data: 'Scores', field: 'data'}}
          ],
          marks: [
            {
              type: 'arc',
              from: {data: 'Scores'},
              properties: {
                enter: {
                  "x": {"group": "width", "mult": 0.5},
                  "y": {"group": "height", "mult": 0.5},
                  "startAngle": {"field": "startAngle"},
                  "endAngle": {"field": "endAngle"},
                  "innerRadius": {"value": 100},
                  "outerRadius": {"scale": "r"},
                  "stroke": {"value": "#fff"}
                },
                update: { fill: {field: 'data.color'}, stroke: {value: '#25292c'}, strokeWidth: {value: '1'}},
                "hover": {"fill": {"value": "#b8b9bc"}}
              }
            },
            {
              type: 'text',
              from: {data: 'Scores'},
              properties: {
                enter: {
                  "x": {"group": "width", "mult": 0.5},
                  "y": {"group": "height", "mult": 0.5},
                  "radius": {"scale": "r", "offset": -70},
                  "theta": {"field": "midAngle"},
                  "fill": {"value": "#fff"},
                  "align": {"value": "center"},
                  "baseline": {"value": "middle"},
                  "text": {"field": "data.y"}
                },
                update: { fill: {field: 'data.color'}, stroke: {value: '#b8b9bc'}, strokeWidth: {value: '1'}}//,
              }
            }
          ]
        };
        vg.parse.spec(spec, function(chart) {
          var view = chart({el: self.$()[0], renderer: 'svg'})
              .update();
        });
      }.observes('data'),
    });

    Explore.PropertyView = Em.View.extend({
      didInsertElement : function(){
        console.log("YO YO YO");
        var self = this;
        Ember.run.next(function(){
          setTimeout(function(){
            var b = self.$('.ratings-affix');
            b.affix({
              offset:{
                top:function(){
                  var c = b.offset().top,
                      d = parseInt(b.children(0).css('margin-top'),10),
                      e = $('.navbar').height();
                  return this.top = c - e - d
                },
                bottom:function(){
                  return this.bottom = $('.footer').outerHeight(!0);
                }
              }
            })
          }, 100);
        });
      },
    });

  });
}(window.jQuery, window.Handlebars, window.Ember, window.d3, window.vg);
