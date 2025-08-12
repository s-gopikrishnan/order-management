package com.gk.ordermanagement.common.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PaymentProcessedEvent implements BaseEvent {

	private String orderId;
	private OrderRequest order;
}
