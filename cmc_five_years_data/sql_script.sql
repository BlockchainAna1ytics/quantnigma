/****** Object:  Table [dbo].[CmcHistoricalPriceData]    Script Date: 2018-08-18 1:24:11 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[CmcHistoricalPriceData](
[Id] [bigint] IDENTITY(1,1) NOT NULL,
[CoinId] [bigint] NOT NULL,
[Symbol] [nvarchar](50) NOT NULL,
[Date] [datetime] NOT NULL,
[Open] [decimal](30, 12) NULL,
[High] [decimal](30, 12) NULL,
[Low] [decimal](30, 12) NULL,
[Close] [decimal](30, 12) NULL,
[Volume] [decimal](30, 12) NULL,
[MarketCap] [bigint] NULL,
 CONSTRAINT [PK_CmcHistoricalPriceData] PRIMARY KEY CLUSTERED 
(
[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [IX_CmcHistoricalPriceData] UNIQUE NONCLUSTERED 
(
[CoinId] ASC,
[Date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[CmcHistoricalPriceData]  WITH CHECK ADD  CONSTRAINT [FK_CmcHistoricalPriceData_CmcCoinListing] FOREIGN KEY([CoinId])
REFERENCES [dbo].[CmcCoinListing] ([CoinId])
GO

ALTER TABLE [dbo].[CmcHistoricalPriceData] CHECK CONSTRAINT [FK_CmcHistoricalPriceData_CmcCoinListing]
GO