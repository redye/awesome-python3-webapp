//
//  APBlog.h
//  AwesomeApp
//
//  Created by redye.hu on 2019/8/2.
//  Copyright © 2019 redye.hu. All rights reserved.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface APBlog : NSObject

@property (strong) NSString* id;

@property (strong) NSString* name;

@property (strong) NSString* summary;

@property (strong) NSString* content;

@property (strong) NSString* user_id;

@property (strong) NSString* user_name;

@property (strong) NSNumber* created_at;

+ (APBlog*) blogWithDictionary:(NSDictionary*) dictionary;

@end

NS_ASSUME_NONNULL_END
