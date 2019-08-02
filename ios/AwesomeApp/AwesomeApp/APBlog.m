//
//  APBlog.m
//  AwesomeApp
//
//  Created by redye.hu on 2019/8/2.
//  Copyright © 2019 redye.hu. All rights reserved.
//

#import "APBlog.h"

@implementation APBlog

+ (APBlog*) blogWithDictionary:(NSDictionary*) dictionary
{
    APBlog* blog = [[APBlog alloc] init];
    blog.id = dictionary[@"id"];
    blog.name = dictionary[@"name"];
    blog.summary = dictionary[@"summary"];
    blog.content = dictionary[@"content"];
    blog.user_id = dictionary[@"user_id"];
    blog.user_name = dictionary[@"user_name"];
    blog.created_at = dictionary[@"created_at"];
    return blog;
}

@end
