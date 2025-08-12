package com.gk.ordermanagement.order.service;

import java.time.LocalDateTime;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import com.gk.ordermanagement.common.models.OrderRequest;
import com.gk.ordermanagement.common.models.PaymentProcessedEvent;
import com.gk.ordermanagement.order.repository.OrderRepository;
import com.gk.ordermanagement.order.model.Order;

@Service
public class OrderEventListener {

	private static final Logger logger = LoggerFactory.getLogger(OrderEventListener.class);

    @Autowired
    private OrderRepository orderRepository;

    @KafkaListener(topics = "payment-processed")
    public void handlePaymentProcessed(PaymentProcessedEvent event) {

    	OrderRequest req = event.getOrder();
    	logger.info("[{}] Inserting Order after processing: {}", req.getOrderId(), req);

        Order order = new Order(req.getOrderId(), req.getCustomerId(), req.getTotalAmount(), "CONFIRMED", req.getPlacedTime(), LocalDateTime.now());
        orderRepository.save(order);
    }
}