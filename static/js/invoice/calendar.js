var calendarEl = document.getElementById('calendar');

var calendar = new FullCalendar.Calendar(calendarEl, {
    navLinks: true,
    dayMaxEvents: true, 

    views: {
      customDayList: {
        type: 'list',
        duration: { days: 1 }, 
        buttonText: 'list'
      },
      timeGrid: {
        dayMaxEventRows: 2 // adjust to 2 or a higher number that works for you
      }
    },
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,customDayList'
    },
    
    displayEventTime: false,
    events: events,
    eventClick: function(info) {
      info.jsEvent.preventDefault();
      var invoice_id = info.event.extendedProps.extraParam1;
      var module_name = info.event.extendedProps.extraParam2;
      console.log("module_name "+module_name)
      if(module_name == 'Invoice Approval'){
        var redirectUrl = '/invoice/invoiceapproval/' + invoice_id; 
      }else if(module_name == 'Tax Confirmation'){
        var redirectUrl = '/invoice/exchangerate/' + invoice_id; 
      }else if(module_name == 'Payment Instruction Generation'){
        var redirectUrl = '/invoice/generatepayment/' + invoice_id; 
      }else if(module_name == 'Payment Instruction Approval'){
        var redirectUrl = '/invoice/signatory/' + invoice_id; 
      }else if(module_name == 'Payment Confirmation'){
        var redirectUrl = '/invoice/accountpayable/' + invoice_id; 
      }
      else if(module_name == 'Bank User'){
        var redirectUrl = '/invoice/bankuserapproval/' + invoice_id; 
      }
      else if(module_name == 'Payment Receipt Upload'){
        var redirectUrl = '/invoice/vendorbasedinvoice'; 
      }
      else if(module_name == 'Invoice Receipt'){
        var redirectUrl = '/invoice/checklist/' + invoice_id; 

      }
      window.location.href = redirectUrl;
    },
    eventContent: function(arg) {
      if (arg.event._def.extendedProps.eventIndex >= 2) {
        return { domNodes: [] }; 
      } else {
        return {
          html: `<span class="fc-event-title">${arg.event.title}</span>` 
        };
      }
    },
    dateClick: function(info) {
      calendar.changeView('customDayList', info.dateStr);
    },


   
});

calendar.render();